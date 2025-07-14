#!/bin/bash

# Collective Memory Setup Script
# Copyright (c) 2025 - MIT License

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                                           ║"
    echo "║                          🧠 Collective Memory v1.0                                       ║"
    echo "║                        Cursor AI Akıllı Bağlam Orkestratörü                              ║"
    echo "║                                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    log_info "Sistem gereksinimleri kontrol ediliyor..."
    
    # Check Docker
    if ! command_exists docker; then
        log_error "Docker bulunamadı! Lütfen Docker'ı yükleyin:"
        echo "  macOS: https://docs.docker.com/desktop/install/mac-install/"
        echo "  Ubuntu: https://docs.docker.com/engine/install/ubuntu/"
        echo "  Windows: https://docs.docker.com/desktop/install/windows-install/"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker çalışmıyor! Lütfen Docker'ı başlatın."
        exit 1
    fi
    
    # Check Python (for local development)
    if ! command_exists python3; then
        log_warning "Python 3 bulunamadı. Sadece Docker modu kullanılabilir."
    fi
    
    # Check Git
    if ! command_exists git; then
        log_warning "Git bulunamadı. Bazı özellikler çalışmayabilir."
    fi
    
    log_success "Sistem gereksinimleri karşılanıyor ✅"
}

# Create necessary directories
create_directories() {
    log_info "Gerekli dizinler oluşturuluyor..."
    
    mkdir -p "${HOME}/.collective-memory"
    mkdir -p "${HOME}/.collective-memory/backups"
    mkdir -p "${HOME}/.collective-memory/logs"
    mkdir -p "${HOME}/.collective-memory/cache"
    
    log_success "Dizinler oluşturuldu ✅"
}

# Build Docker image
build_docker_image() {
    log_info "Docker image oluşturuluyor..."
    
    if docker build -t collective-memory:latest .; then
        log_success "Docker image başarıyla oluşturuldu ✅"
    else
        log_error "Docker image oluşturulamadı!"
        exit 1
    fi
}

# Install collect-memory command
install_command() {
    log_info "collect-memory komutu yükleniyor..."
    
    # Create the wrapper script
    cat > "${HOME}/.collective-memory/collect-memory" << 'EOF'
#!/bin/bash

# Collective Memory Wrapper Script
# This script runs the Collective Memory Docker container

# Get current directory
CURRENT_DIR="$(pwd)"
PROJECT_NAME="$(basename "$CURRENT_DIR")"

# Check if we're in a valid directory
if [ ! -d ".git" ] && [ ! -f "package.json" ] && [ ! -f "requirements.txt" ] && [ ! -f "Cargo.toml" ]; then
    echo "⚠️  Bu dizin bir proje klasörü gibi görünmüyor."
    echo "   Git deposu, package.json, requirements.txt veya Cargo.toml dosyası bulunamadı."
    echo "   Yine de devam etmek istiyor musunuz? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "İşlem iptal edildi."
        exit 1
    fi
fi

# Run Docker container
docker run --rm \
    -v "$CURRENT_DIR:/workspace" \
    -v "$HOME/.collective-memory:/app/data" \
    -v "$HOME/Library/Application Support/Cursor:/cursor-data:ro" \
    -v "$HOME/.config/Cursor:/cursor-config:ro" \
    -w /workspace \
    collective-memory:latest "$@"
EOF

    chmod +x "${HOME}/.collective-memory/collect-memory"
    
    # Add to PATH
    SHELL_RC=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    # Check if already in PATH
    if ! grep -q "collective-memory" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# Collective Memory" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.collective-memory:\$PATH\"" >> "$SHELL_RC"
        log_success "collect-memory komutu PATH'e eklendi ✅"
        log_info "Değişikliklerin geçerli olması için terminali yeniden başlatın veya:"
        echo "  source $SHELL_RC"
    else
        log_info "collect-memory komutu zaten PATH'de mevcut"
    fi
}

# Test installation
test_installation() {
    log_info "Kurulum test ediliyor..."
    
    # Test Docker image
    if docker run --rm collective-memory:latest --version >/dev/null 2>&1; then
        log_success "Docker image testi başarılı ✅"
    else
        log_error "Docker image testi başarısız!"
        exit 1
    fi
    
    # Test wrapper script
    if "${HOME}/.collective-memory/collect-memory" --help >/dev/null 2>&1; then
        log_success "Wrapper script testi başarılı ✅"
    else
        log_error "Wrapper script testi başarısız!"
        exit 1
    fi
}

# Create example files
create_examples() {
    log_info "Örnek dosyalar oluşturuluyor..."
    
    # Example Python file
    cat > "${HOME}/.collective-memory/example.py" << 'EOF'
#!/usr/bin/env python3
"""
Collective Memory Örnek Dosya
"""

# @collect-memory: Bu Python dosyasını analiz et ve geliştirme önerileri sun

def main():
    print("Merhaba Collective Memory!")
    
    # Bu fonksiyon geliştirilebilir
    # Daha fazla özellik eklenebilir
    
if __name__ == "__main__":
    main()
EOF

    # Example usage guide
    cat > "${HOME}/.collective-memory/USAGE.md" << 'EOF'
# Collective Memory Kullanım Kılavuzu

## Hızlı Başlangıç

1. **Proje klasörüne gidin:**
   ```bash
   cd your-project-directory
   ```

2. **Kod içine tetikleyici ekleyin:**
   ```python
   # @collect-memory: Bu fonksiyon nasıl optimize edilebilir?
   def my_function():
       pass
   ```

3. **Komutu çalıştırın:**
   ```bash
   collect-memory --scan
   ```

4. **Sonucu Cursor'a yapıştırın ve kullanın!**

## Komutlar

- `collect-memory --scan` - Proje içinde tetikleyici ara
- `collect-memory --request "Your request"` - Manuel istek
- `collect-memory --help` - Yardım
- `collect-memory --version` - Sürüm bilgisi

## Desteklenen Dosya Türleri

- Python: `# @collect-memory: İsteğiniz`
- JavaScript/TypeScript: `// @collect-memory: İsteğiniz`
- Java: `// @collect-memory: İsteğiniz`
- HTML: `<!-- @collect-memory: İsteğiniz -->`
- CSS: `/* @collect-memory: İsteğiniz */`
- SQL: `-- @collect-memory: İsteğiniz`
- YAML: `# @collect-memory: İsteğiniz`

## Daha Fazla Bilgi

GitHub: https://github.com/your-username/collective-memory
EOF

    log_success "Örnek dosyalar oluşturuldu ✅"
    log_info "Örnekler: ~/.collective-memory/ klasöründe"
}

# Main installation function
main() {
    print_banner
    
    log_info "Collective Memory kurulumu başlıyor..."
    echo
    
    # Check requirements
    check_requirements
    
    # Create directories
    create_directories
    
    # Build Docker image
    build_docker_image
    
    # Install command
    install_command
    
    # Test installation
    test_installation
    
    # Create examples
    create_examples
    
    echo
    log_success "🎉 Collective Memory başarıyla kuruldu!"
    echo
    echo -e "${CYAN}Sonraki adımlar:${NC}"
    echo "1. Terminali yeniden başlatın veya: source ~/.bashrc (veya ~/.zshrc)"
    echo "2. Proje klasörünüze gidin: cd your-project"
    echo "3. Kod içine tetikleyici ekleyin: # @collect-memory: Your request"
    echo "4. Komutu çalıştırın: collect-memory --scan"
    echo "5. Sonucu Cursor'a yapıştırın!"
    echo
    echo -e "${YELLOW}Daha fazla bilgi: ~/.collective-memory/USAGE.md${NC}"
    echo
}

# Run main function
main "$@" 