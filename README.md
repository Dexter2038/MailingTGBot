# 📧 MailingTGBot

A Telegram bot written in **aiogram v3** for managing mailing operations from admins to users with a comprehensive hierarchical permission system.

## 🎯 Features

- **👑 Admin Management** - Full admin control with role-based access
- **👥 Sub-Admin Management** - Delegate administrative tasks to sub-administrators  
- **🛡️ Moderator Management** - Moderation system for user management
- **📬 Mailing System** - Send messages to users with full tracking capabilities
- **🔐 Role-Based Access Control** - Hierarchical permission system (Admin → Sub-admin → Moderator → User)
- **💾 Database Integration** - MySQL support via TinyDB
- **🔧 Async/Await Architecture** - Fully asynchronous for high performance
- **🐳 Docker Support** - Easy deployment with Docker

## 📋 Prerequisites

- Python 3.12.6 or higher
- MySQL database
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- (Optional) Google API credentials for integration

## 🚀 Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dexter2038/MailingTGBot.git
   cd MailingTGBot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   BOT_TOKEN=your_bot_token_here
   DB_HOST=localhost
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   MAIL_USERNAME=your_mail_username
   ADMIN=admin_user_id
   ```

5. **Run the bot:**
   ```bash
   python -m app
   ```

### Docker Setup

1. **Build the image:**
   ```bash
   docker build -t mailing-tgbot .
   ```

2. **Run the container:**
   ```bash
   docker run -e BOT_TOKEN=your_token \
              -e DB_HOST=your_db_host \
              -e DB_USER=your_db_user \
              -e DB_PASSWORD=your_db_password \
              -e DB_NAME=your_db_name \
              -e ADMIN=your_admin_id \
              mailing-tgbot
   ```

## 📁 Project Structure

```
MailingTGBot/
├── app/
│   ├── config/          # Configuration and initialization
│   ├── handlers/        # Command and message handlers
│   │   ├── root.py      # Admin handlers
│   │   ├── subadmins.py # Sub-admin handlers
│   │   ├── moders.py    # Moderator handlers
│   │   ├── users.py     # User handlers
│   │   └── chat.py      # Chat-related handlers
│   ├── database/        # Database models and operations
│   ├── utils/           # Utility functions
│   └── __main__.py      # Application entry point
├── requirements.txt     # Project dependencies
├── dockerfile          # Docker configuration
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram Bot API token | ✅ |
| `DB_HOST` | Database hostname | ✅ |
| `DB_USER` | Database username | ✅ |
| `DB_PASSWORD` | Database password | ✅ |
| `DB_NAME` | Database name | ✅ |
| `ADMIN` | Initial admin user ID | ✅ |
| `MAIL_USERNAME` | Email for mailing service | ⚠️ |

## 📦 Key Dependencies

- **aiogram** (3.13.1) - Telegram Bot API framework
- **aiohttp** (3.10.10) - Async HTTP client
- **sqlalchemy** - ORM for database operations
- **pydantic** (2.9.2) - Data validation
- **PyYAML** (6.0.2) - Configuration management
- **python-dotenv** (1.0.1) - Environment variable management
- **Pyrogram** (2.0.106) - MTProto API client
- **google-api-python-client** - Google API integration

## 🎮 Usage

### Admin Commands

- `/start` - Initialize the bot
- `/admin` - Access admin panel
- `/send_mail` - Send mailing to users
- `/manage_admins` - Manage sub-administrators

### Sub-Admin Commands

- Access delegated admin functions
- `/manage_moderators` - Manage moderator team

### Moderator Commands

- `/moderate` - Access moderation tools
- `/manage_users` - Manage user accounts

### User Commands

- `/start` - Bot introduction
- `/help` - Get help information
- `/menu` - Main menu

## 🔄 Architecture

The bot uses a hierarchical handler structure:

1. **Root Router** - Main admin commands
2. **Sub-Admin Router** - Sub-administrator functions
3. **Moderator Router** - Moderation tools
4. **User Router** - Standard user commands
5. **Chat Router** - Chat-specific handling

All handlers are combined in a single router that processes incoming updates from Telegram.

## 🗄️ Database

The project uses MySQL database with the following features:

- User profiles and roles
- Admin/Sub-admin/Moderator management
- Mailing logs and statistics
- Custom rank system

Database is initialized automatically on first run via `app.database.models.init_db()`.

## 🛡️ Security Features

- Role-based access control (RBAC)
- Admin ID verification
- Permission-based command execution
- Environment variable-based configuration (no hardcoded secrets)

## 🐛 Troubleshooting

### Bot Token not found
```
Exception: Переменная окружения 'BOT_TOKEN' не найдена
```
**Solution:** Set the `BOT_TOKEN` environment variable before running.

### Database connection failed
**Solution:** Verify database credentials and ensure MySQL is running:
```bash
mysql -h your_host -u your_user -p
```

### Import errors
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## 📝 License

This project is open source. Feel free to fork and contribute!

## 👨‍💻 Author

**Dexter2038**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the repository owner.

---

**Made with ❤️ using aiogram**
