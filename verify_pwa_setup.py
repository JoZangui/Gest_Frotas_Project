#!/usr/bin/env python
"""
Script de verificação da implementação PWA
Execute: python verify_pwa_setup.py
"""

import os
import json
import sys
from pathlib import Path

class PWAVerifier:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.warnings = []
        self.success_count = 0

    def check_file_exists(self, file_path, description):
        """Verificar se um arquivo existe"""
        full_path = self.project_root / file_path
        if full_path.exists():
            self.success_count += 1
            print(f"✅ {description}: {file_path}")
            return True
        else:
            self.issues.append(f"❌ Arquivo não encontrado: {file_path}")
            print(f"❌ {description}: {file_path}")
            return False

    def check_file_contains(self, file_path, search_text, description):
        """Verificar se um arquivo contém um texto específico"""
        full_path = self.project_root / file_path
        if not full_path.exists():
            self.issues.append(f"❌ Arquivo não encontrado: {file_path}")
            return False
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if search_text in content:
                    self.success_count += 1
                    print(f"✅ {description}")
                    return True
                else:
                    self.issues.append(f"❌ {description} - texto não encontrado em {file_path}")
                    print(f"❌ {description}")
                    return False
        except Exception as e:
            self.issues.append(f"❌ Erro ao ler {file_path}: {str(e)}")
            return False

    def check_json_valid(self, file_path, description):
        """Verificar se um arquivo JSON é válido"""
        full_path = self.project_root / file_path
        if not full_path.exists():
            self.issues.append(f"❌ Arquivo JSON não encontrado: {file_path}")
            return False
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                json.load(f)
                self.success_count += 1
                print(f"✅ {description}: JSON válido")
                return True
        except json.JSONDecodeError as e:
            self.issues.append(f"❌ JSON inválido em {file_path}: {str(e)}")
            print(f"❌ {description}: JSON inválido")
            return False

    def run_all_checks(self):
        """Executar todas as verificações"""
        print("\n" + "="*60)
        print("🔍 VERIFICAÇÃO DA IMPLEMENTAÇÃO PWA")
        print("="*60 + "\n")

        print("📦 Verificando Arquivos de Configuração PWA:\n")
        self.check_file_exists("static/js/manifest.json", "Manifest")
        self.check_json_valid("static/js/manifest.json", "Manifest JSON")
        
        print("\n🔄 Verificando Service Worker:\n")
        self.check_file_exists("static/js/service-worker.js", "Service Worker")
        self.check_file_contains(
            "static/js/service-worker.js", 
            "self.addEventListener('install'",
            "Install event no Service Worker"
        )
        self.check_file_contains(
            "static/js/service-worker.js",
            "self.addEventListener('fetch'",
            "Fetch event no Service Worker"
        )

        print("\n📍 Verificando Script de Geolocalização:\n")
        self.check_file_exists("static/js/geolocation.js", "Geolocation Script")
        self.check_file_contains(
            "static/js/geolocation.js",
            "class GeolocationTracker",
            "Classe GeolocationTracker"
        )
        self.check_file_contains(
            "static/js/geolocation.js",
            "navigator.geolocation.watchPosition",
            "Watch Position no Geolocation"
        )

        print("\n🎨 Verificando Templates:\n")
        self.check_file_exists("gest_frotas_app/templates/gest_frotas_app/base.html", "Base HTML")
        self.check_file_exists("gest_frotas_app/templates/gest_frotas_app/rastreamento_painel.html", "Painel HTML")
        self.check_file_contains(
            "gest_frotas_app/templates/gest_frotas_app/base.html",
            "geolocation.js",
            "Geolocation script no Base HTML"
        )
        self.check_file_contains(
            "gest_frotas_app/templates/gest_frotas_app/base.html",
            "service-worker.js",
            "Service Worker no Base HTML"
        )

        print("\n📡 Verificando Views do Django:\n")
        self.check_file_contains(
            "gest_frotas_app/views.py",
            "def receber_localizacao",
            "View receber_localizacao"
        )
        self.check_file_contains(
            "gest_frotas_app/views.py",
            "def listar_localizacoes",
            "View listar_localizacoes"
        )
        self.check_file_contains(
            "gest_frotas_app/views.py",
            "def obter_ultimo_rastreamento",
            "View obter_ultimo_rastreamento"
        )
        self.check_file_contains(
            "gest_frotas_app/views.py",
            "def rastreamento_painel",
            "View rastreamento_painel"
        )

        print("\n🌐 Verificando URLs:\n")
        self.check_file_contains(
            "gest_frotas_app/urls.py",
            "receber_localizacao",
            "URL receber_localizacao"
        )
        self.check_file_contains(
            "gest_frotas_app/urls.py",
            "rastreamento_painel",
            "URL rastreamento_painel"
        )

        print("\n📚 Verificando Documentação:\n")
        self.check_file_exists("PWA_GUIDE.md", "PWA Guide")
        self.check_file_exists("IMPLEMENTATION_SUMMARY.md", "Implementation Summary")

        print("\n" + "="*60)
        print("📊 RESULTADO DA VERIFICAÇÃO")
        print("="*60)
        print(f"\n✅ Verificações bem-sucedidas: {self.success_count}")
        
        if self.issues:
            print(f"❌ Problemas encontrados: {len(self.issues)}\n")
            for issue in self.issues:
                print(f"  {issue}")
        
        if self.warnings:
            print(f"\n⚠️  Avisos: {len(self.warnings)}\n")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.issues:
            print("\n🎉 TUDO OK! A implementação PWA foi concluída com sucesso!\n")
            return True
        else:
            print(f"\n⚠️  Existem {len(self.issues)} problemas a resolver.\n")
            return False

    def print_next_steps(self):
        """Imprimir próximos passos"""
        print("="*60)
        print("🚀 PRÓXIMOS PASSOS")
        print("="*60 + "\n")
        
        print("1. Iniciar o servidor Django:")
        print("   $ python manage.py runserver 0.0.0.0:8000\n")
        
        print("2. Acessar no navegador:")
        print("   - Desktop: http://localhost:8000/")
        print("   - Smartphone: http://SEU_IP:8000/\n")
        
        print("3. Aceitar permissões:")
        print("   - Localização (GPS)")
        print("   - Notificações\n")
        
        print("4. Acessar o painel de controle:")
        print("   http://localhost:8000/rastreamento/\n")
        
        print("5. Verificar dados no Admin:")
        print("   http://localhost:8000/admin/\n")
        
        print("6. Para produção:")
        print("   - Usar HTTPS obrigatoriamente")
        print("   - Configurar ALLOWED_HOSTS")
        print("   - Definir DEBUG = False\n")


def main():
    # Determinar caminho do projeto
    project_root = Path(__file__).parent
    
    verifier = PWAVerifier(project_root)
    success = verifier.run_all_checks()
    verifier.print_next_steps()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
