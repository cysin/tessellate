#!/usr/bin/env python3
"""
密码设置工具 / Password Setup Utility

用于生成密码哈希并配置认证系统。
This script helps you generate a password hash and configure the authentication system.

使用方法 / Usage:
    python setup_password.py
"""

import os
import sys
import secrets
import getpass
from werkzeug.security import generate_password_hash


def validate_password(password):
    """验证密码强度 / Validate password strength"""
    if len(password) < 8:
        return False, "密码长度必须至少8个字符 / Password must be at least 8 characters"
    return True, ""


def generate_secret_key():
    """生成安全的密钥 / Generate secure secret key"""
    return secrets.token_hex(32)


def create_env_file(password_hash, secret_key, session_lifetime=86400):
    """创建.env文件 / Create .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')

    # 检查是否已存在.env文件 / Check if .env exists
    if os.path.exists(env_path):
        response = input("\n⚠️  .env文件已存在。是否覆盖？(y/N) / .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ 操作已取消 / Operation cancelled")
            return False

    # 写入.env文件 / Write .env file
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write("# Authentication Configuration\n")
        f.write("# 认证配置\n\n")
        f.write(f"APP_PASSWORD_HASH={password_hash}\n")
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write(f"SESSION_LIFETIME={session_lifetime}\n")
        f.write("ENVIRONMENT=production\n")

    # 设置文件权限（仅所有者可读写） / Set file permissions
    try:
        os.chmod(env_path, 0o600)
    except:
        pass  # Windows可能不支持 / Windows might not support this

    return True


def main():
    """主函数 / Main function"""
    print("=" * 60)
    print("🔐 家具板材下料系统 - 密码设置")
    print("   Furniture Cutting System - Password Setup")
    print("=" * 60)
    print()

    # 获取密码 / Get password
    while True:
        print("请输入访问密码（至少8个字符）：")
        print("Please enter access password (minimum 8 characters):")
        password = getpass.getpass("密码 / Password: ")

        # 验证密码 / Validate password
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            print(f"❌ {error_msg}\n")
            continue

        # 确认密码 / Confirm password
        print("\n请再次输入密码确认：")
        print("Please enter password again to confirm:")
        password_confirm = getpass.getpass("确认密码 / Confirm password: ")

        if password != password_confirm:
            print("❌ 两次输入的密码不一致 / Passwords do not match\n")
            continue

        break

    print("\n⏳ 正在生成密码哈希... / Generating password hash...")
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    print("⏳ 正在生成会话密钥... / Generating session secret key...")
    secret_key = generate_secret_key()

    # 询问会话超时时间 / Ask for session timeout
    print("\n会话超时时间设置 / Session timeout settings:")
    print("1. 1小时 / 1 hour")
    print("2. 8小时 / 8 hours")
    print("3. 24小时 / 24 hours (推荐 / recommended)")
    print("4. 7天 / 7 days")

    timeout_options = {
        '1': 3600,
        '2': 28800,
        '3': 86400,
        '4': 604800
    }

    while True:
        choice = input("\n请选择 (1-4，默认3) / Choose (1-4, default 3): ").strip()
        if not choice:
            choice = '3'
        if choice in timeout_options:
            session_lifetime = timeout_options[choice]
            break
        print("❌ 无效选择 / Invalid choice")

    # 创建.env文件 / Create .env file
    print("\n⏳ 正在创建配置文件... / Creating configuration file...")
    if create_env_file(password_hash, secret_key, session_lifetime):
        print("\n" + "=" * 60)
        print("✅ 密码设置成功！/ Password setup successful!")
        print("=" * 60)
        print()
        print("配置已保存到 .env 文件 / Configuration saved to .env file")
        print()
        print("下一步 / Next steps:")
        print("1. 安装依赖 / Install dependencies:")
        print("   pip install -r requirements.txt")
        print()
        print("2. 启动服务器 / Start server:")
        print("   python app.py")
        print()
        print("3. 访问系统 / Access system:")
        print("   http://localhost:5000")
        print()
        print("⚠️  重要 / Important:")
        print("   - 请妥善保管您的密码 / Please keep your password safe")
        print("   - 不要提交 .env 文件到版本控制系统")
        print("   - Do not commit .env file to version control")
        print("   - 建议在生产环境使用HTTPS")
        print("   - It is recommended to use HTTPS in production")
        print("=" * 60)
        return 0
    else:
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ 操作已取消 / Operation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误 / Error: {e}")
        sys.exit(1)
