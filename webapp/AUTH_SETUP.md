# 认证系统设置指南 / Authentication Setup Guide

本文档介绍如何为家具板材智能下料系统配置密码保护。
This document explains how to configure password protection for the Furniture Cutting System.

---

## 🔐 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
cd webapp
pip install -r requirements.txt
```

### 2. 设置密码 / Setup Password

运行密码设置工具：
```bash
python setup_password.py
```

按照提示操作：
1. 输入您想设置的访问密码（至少8个字符）
2. 再次输入密码确认
3. 选择会话超时时间（推荐24小时）

脚本将自动生成：
- `.env` 文件（包含密码哈希和会话密钥）
- 安全的随机密钥用于会话加密

### 3. 启动服务器 / Start Server

```bash
python app.py
```

### 4. 访问系统 / Access System

打开浏览器访问：`http://localhost:5000`

系统将自动跳转到登录页面，输入您设置的密码即可访问。

---

## 📋 配置详解 / Configuration Details

### 环境变量 / Environment Variables

认证系统使用 `.env` 文件存储配置：

```env
# 密码哈希（由 setup_password.py 生成）
APP_PASSWORD_HASH=pbkdf2:sha256:...

# 会话密钥（由 setup_password.py 生成）
SECRET_KEY=随机生成的密钥

# 会话生命周期（秒）
SESSION_LIFETIME=86400  # 24小时

# 环境设置
ENVIRONMENT=production
```

**重要提示：**
- ⚠️ 切勿将 `.env` 文件提交到版本控制系统
- ⚠️ 定期更换密码和密钥
- ⚠️ 在生产环境中使用HTTPS

---

## 🔄 常见操作 / Common Operations

### 修改密码 / Change Password

1. 重新运行 `python setup_password.py`
2. 输入新密码
3. 确认覆盖现有配置
4. 重启服务器

### 重置密码 / Reset Password

如果忘记密码：

1. 停止服务器
2. 删除 `.env` 文件：`rm .env`
3. 重新运行 `python setup_password.py` 设置新密码
4. 启动服务器

### 更改会话超时时间 / Change Session Timeout

编辑 `.env` 文件，修改 `SESSION_LIFETIME` 值（单位：秒）：

```env
SESSION_LIFETIME=3600    # 1小时
SESSION_LIFETIME=28800   # 8小时
SESSION_LIFETIME=86400   # 24小时（推荐）
SESSION_LIFETIME=604800  # 7天
```

修改后重启服务器。

### 禁用认证（仅开发环境）/ Disable Authentication (Development Only)

在 `.env` 文件中设置：
```env
ENVIRONMENT=development
```

并删除或注释 `APP_PASSWORD_HASH` 行。

**⚠️ 切勿在生产环境禁用认证！**

---

## 🔒 安全最佳实践 / Security Best Practices

### 1. 密码强度 / Password Strength

推荐密码要求：
- ✅ 至少 12 个字符
- ✅ 包含大小写字母
- ✅ 包含数字
- ✅ 包含特殊字符

### 2. HTTPS 配置 / HTTPS Setup

**生产环境必须使用 HTTPS！**

方法 1：使用反向代理（推荐）
```nginx
# Nginx 配置示例
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

方法 2：使用 Cloudflare
- 将您的域名接入 Cloudflare
- 启用 SSL/TLS 加密
- 后端服务器仍使用 HTTP（Cloudflare 到客户端使用 HTTPS）

### 3. 文件权限 / File Permissions

确保 `.env` 文件只有所有者可读：
```bash
chmod 600 .env
```

### 4. 登录保护 / Login Protection

系统已内置：
- ✅ 登录速率限制（15分钟内最多5次尝试）
- ✅ 密码哈希存储（使用 PBKDF2-SHA256）
- ✅ 会话管理（服务器端存储）
- ✅ CSRF 保护
- ✅ HttpOnly Cookie

---

## 🛠️ 故障排除 / Troubleshooting

### 问题：无法登录 / Cannot Login

**症状：** 输入正确密码后仍提示错误

**解决方案：**
1. 检查 `.env` 文件是否存在
2. 确认 `APP_PASSWORD_HASH` 配置正确
3. 重新运行 `python setup_password.py`
4. 清除浏览器缓存和 Cookie
5. 检查服务器日志

### 问题：会话频繁过期 / Session Expires Frequently

**症状：** 短时间内需要重复登录

**解决方案：**
1. 检查 `SESSION_LIFETIME` 配置
2. 确认服务器时间正确
3. 检查 `flask_session/` 目录权限
4. 增加 `SESSION_LIFETIME` 值

### 问题："Too many login attempts"

**症状：** 提示登录尝试次数过多

**解决方案：**
1. 等待 15 分钟后重试
2. 或重启服务器清除速率限制计数

### 问题：密码哈希生成失败 / Password Hash Generation Failed

**症状：** 运行 `setup_password.py` 时出错

**解决方案：**
1. 确认已安装 `werkzeug`：`pip install werkzeug`
2. 检查 Python 版本（需要 3.7+）
3. 查看详细错误信息

---

## 📖 技术细节 / Technical Details

### 认证流程 / Authentication Flow

1. **用户访问** → 检查会话 → 未认证则跳转登录页
2. **输入密码** → 发送到 `/api/login`
3. **服务器验证** → 检查速率限制 → 验证密码哈希
4. **创建会话** → 设置 `authenticated=True`
5. **访问授权** → 所有请求检查会话状态

### 会话存储 / Session Storage

- 类型：服务器端文件存储
- 位置：`flask_session/` 目录
- 过期：根据 `SESSION_LIFETIME` 自动清理
- 安全：HttpOnly, SameSite=Lax

### 密码哈希算法 / Password Hashing

- 算法：PBKDF2-SHA256
- 迭代次数：260000（Werkzeug 默认）
- 盐值：自动生成（每个哈希唯一）

---

## 📞 支持 / Support

如有问题，请：
1. 查看本文档故障排除部分
2. 检查服务器日志
3. 参考 Flask 和 Flask-Session 官方文档

---

**最后更新：** 2025-11-11
**版本：** 1.0
