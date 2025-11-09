# 🌐 Tessellate Web Application

Beautiful, modern web interface for the Tessellate 2D Guillotine Cutting Stock Optimizer.

## 🚀 Quick Start

### Option 1: Using Startup Scripts (Recommended)

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

The scripts will automatically:
- Create a virtual environment (if needed)
- Install all dependencies
- Start the Flask server on http://localhost:5000

### Option 2: Manual Setup

**1. Create and activate virtual environment:**

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```batch
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the application:**
```bash
python app.py
```

**4. Open your browser:**
```
http://localhost:5000
```

## 📁 Directory Structure

```
webapp/
├── venv/              # Virtual environment (auto-created)
├── app.py             # Flask application server
├── requirements.txt   # Python dependencies
├── start.sh          # Linux/Mac startup script
├── start.bat         # Windows startup script
├── .gitignore        # Git ignore rules
├── templates/
│   └── index.html    # Main web interface
├── static/           # (Future: CSS/JS files)
│   ├── css/
│   └── js/
└── api/              # (Future: API modules)
    └── routes.py
```

## 🎨 Features

### Web Interface
- **Beautiful Modern UI**: Gradient design, responsive layout
- **Interactive Input**: JSON-based problem specification
- **Live Visualization**: SVG rendering of cutting patterns
- **Real-Time Metrics**: Bins used, utilization %, execution time
- **Example Loader**: Pre-built examples to get started

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/solve` | POST | Solve a cutting stock problem |
| `/api/example` | GET | Get example problem JSON |
| `/api/health` | GET | Health check endpoint |
| `/api/validate` | POST | Validate a solution |

## 🔌 API Usage

### Solve a Problem

**Request:**
```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d @problem.json
```

**Response:**
```json
{
  "metadata": {
    "objectiveValue": 2,
    "utilization": 0.823,
    "executionTime": 0.125,
    "algorithmName": "MaxRects-Lookahead-2"
  },
  "bins": [...],
  "unplaced": []
}
```

### Get Example Problem

**Request:**
```bash
curl http://localhost:5000/api/example
```

**Response:**
```json
{
  "items": [...],
  "bins": [...],
  "parameters": {...}
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the webapp directory:

```bash
# Server configuration
PORT=5000
DEBUG=True

# Flask settings
FLASK_APP=app.py
FLASK_ENV=development
```

### Custom Port

**Using environment variable:**
```bash
PORT=8080 python app.py
```

**Or modify app.py:**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

## 🖥️ Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge (v90+)
- ✅ Firefox (v88+)
- ✅ Safari (v14+)

## 🔒 Security Notes

For production deployment:
1. Set `DEBUG=False` in environment variables
2. Use a production WSGI server (gunicorn, uWSGI)
3. Enable HTTPS
4. Add rate limiting
5. Implement authentication if needed

## 🚢 Production Deployment

### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t tessellate-webapp .
docker run -p 5000:5000 tessellate-webapp
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
PORT=8080 python app.py
```

### Import Errors
Make sure you're in the webapp directory and the parent tessellate library is accessible:
```bash
cd webapp
python app.py
```

### Dependencies Not Found
Activate the virtual environment first:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 📊 Performance

- **Typical response time**: 50-200ms for problems with <50 items
- **Large problems**: 1-5s for 100+ items
- **Concurrent requests**: Supports multiple simultaneous requests
- **Memory usage**: ~50-100MB per request

## 🔄 Development

### Hot Reload

Flask debug mode enables auto-reload on code changes:
```bash
DEBUG=True python app.py
```

### Adding New Endpoints

Edit `app.py` and add new routes:
```python
@app.route('/api/custom', methods=['POST'])
def custom_endpoint():
    # Your code here
    return jsonify({"result": "success"})
```

## 📝 License

MIT License - See parent directory LICENSE file

## 🤝 Contributing

1. Make changes in a feature branch
2. Test thoroughly with various problem sizes
3. Update documentation
4. Submit pull request

## 📞 Support

- Documentation: See parent `README_TESSELLATE.md`
- Issues: Report on GitHub
- Examples: Check `../benchmarks/` directory

---

**Happy Optimizing! 🎯**
