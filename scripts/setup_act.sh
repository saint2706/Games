#!/bin/bash
# Script to install act (GitHub Actions local runner)
# This allows you to run and debug GitHub Actions workflows locally

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}GitHub Actions Local Runner (act) Setup${NC}"
echo "=========================================="
echo ""

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Check if act is already installed
if command -v act &> /dev/null; then
    CURRENT_VERSION=$(act --version | grep -oP 'act version \K[0-9.]+' || echo "unknown")
    echo -e "${GREEN}✓ act is already installed (version: $CURRENT_VERSION)${NC}"
    echo ""
    echo "To upgrade act:"
    if [ "$OS" = "macos" ]; then
        echo "  brew upgrade act"
    elif [ "$OS" = "linux" ]; then
        echo "  Run this script again to download the latest version"
    fi
    echo ""
    exit 0
fi

echo -e "${YELLOW}Installing act...${NC}"
echo ""

# Install based on OS
case "$OS" in
    "macos")
        echo "Installing via Homebrew..."
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}Error: Homebrew not found. Please install Homebrew first:${NC}"
            echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        brew install act
        ;;
    
    "linux")
        echo "Installing via GitHub release..."
        # Download latest release
        LATEST_VERSION=$(curl -s https://api.github.com/repos/nektos/act/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
        
        if [ -z "$LATEST_VERSION" ]; then
            echo -e "${RED}Error: Failed to get latest version${NC}"
            exit 1
        fi
        
        echo "Downloading act v${LATEST_VERSION}..."
        
        # Detect architecture
        ARCH=$(uname -m)
        if [ "$ARCH" = "x86_64" ]; then
            ARCH="x86_64"
        elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
            ARCH="arm64"
        else
            echo -e "${RED}Error: Unsupported architecture: $ARCH${NC}"
            exit 1
        fi
        
        DOWNLOAD_URL="https://github.com/nektos/act/releases/download/v${LATEST_VERSION}/act_Linux_${ARCH}.tar.gz"
        
        # Download and install
        TMP_DIR=$(mktemp -d)
        cd "$TMP_DIR"
        
        curl -L -o act.tar.gz "$DOWNLOAD_URL"
        tar xzf act.tar.gz
        
        # Install to user's local bin
        mkdir -p "$HOME/.local/bin"
        mv act "$HOME/.local/bin/"
        chmod +x "$HOME/.local/bin/act"
        
        # Clean up
        cd -
        rm -rf "$TMP_DIR"
        
        # Add to PATH if not already there
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo ""
            echo -e "${YELLOW}Note: Add the following to your ~/.bashrc or ~/.zshrc:${NC}"
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            export PATH="$HOME/.local/bin:$PATH"
        fi
        ;;
    
    "windows")
        echo "For Windows, please install using one of these methods:"
        echo ""
        echo "1. Using Chocolatey:"
        echo "   choco install act-cli"
        echo ""
        echo "2. Using Scoop:"
        echo "   scoop install act"
        echo ""
        echo "3. Using winget:"
        echo "   winget install nektos.act"
        echo ""
        echo "4. Manual download from:"
        echo "   https://github.com/nektos/act/releases"
        exit 0
        ;;
    
    *)
        echo -e "${RED}Error: Unsupported operating system${NC}"
        exit 1
        ;;
esac

# Verify installation
if command -v act &> /dev/null; then
    VERSION=$(act --version | grep -oP 'act version \K[0-9.]+' || echo "unknown")
    echo ""
    echo -e "${GREEN}✓ Successfully installed act version $VERSION${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run workflows with: ./scripts/run_workflow.sh"
    echo "2. See documentation: docs/development/LOCAL_WORKFLOWS.md"
else
    echo -e "${RED}Error: Installation failed${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}act installation complete!${NC}"
