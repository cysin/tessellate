# GV Application - Quick Start Guide

## Prerequisites

Before running the GV application, ensure you have:

- ✓ **Java JDK 7 or higher** installed
- ✓ **Apache Tomcat 8.5.x** installed (already available at `/home/star/work/apache-tomcat-8.5.57`)
- ✓ Terminal/command line access

## Quick Start (3 Steps)

### Step 1: Build the Application

```bash
cd /home/star/work/apache-tomcat-8.5.57/GV-recovered-source
./build.sh
```

This will:
- Compile all Java source files
- Create WAR file structure
- Package everything into `dist/GV.war`

**Expected output:**
```
[1/5] Cleaning previous build...
[2/5] Compiling Java sources...
   ✓ Compilation successful
[3/5] Creating WAR structure...
[4/5] Creating WAR file...
   ✓ WAR file created: GV.war (9.2M)
[5/5] Build Summary
✓ Build completed successfully!
```

### Step 2: Deploy to Tomcat

```bash
./deploy.sh
```

This will:
- Copy WAR file to Tomcat webapps directory
- Auto-deploy if Tomcat is running
- Create backup of existing deployment

**Expected output:**
```
[1/4] Checking Tomcat installation...
   ✓ Found Tomcat
[2/4] Checking for existing deployment...
[3/4] Deploying application...
   ✓ WAR file copied
[4/4] Checking Tomcat status...
   ✓ Application deployed successfully!
```

### Step 3: Access the Application

Open your browser and navigate to:

```
http://localhost:8089/GV/input.jsp
```

**Note:** Check your Tomcat `server.xml` for the correct port (8088 or 8089).

---

## Detailed Setup Instructions

### Option A: Automated Build & Deploy (Recommended)

```bash
# Navigate to the project directory
cd /home/star/work/apache-tomcat-8.5.57/GV-recovered-source

# Build the application
./build.sh

# Deploy to Tomcat
./deploy.sh

# Start Tomcat (if not running)
/home/star/work/apache-tomcat-8.5.57/bin/startup.sh

# Watch deployment logs
tail -f /home/star/work/apache-tomcat-8.5.57/logs/catalina.out
```

### Option B: Manual Build & Deploy

#### 1. Compile Java Sources

```bash
cd GV-recovered-source

# Clean build directory
rm -rf build dist
mkdir -p build

# Set classpath
CLASSPATH=""
for jar in lib/*.jar; do
    CLASSPATH="$CLASSPATH:$jar"
done
CLASSPATH="$CLASSPATH:/home/star/work/apache-tomcat-8.5.57/lib/servlet-api.jar"

# Compile
javac -encoding UTF-8 \
      -cp "$CLASSPATH" \
      -d build \
      -sourcepath src \
      src/com/gv/**/*.java \
      src/*.java
```

#### 2. Create WAR File

```bash
# Create WAR structure
mkdir -p dist/GV/WEB-INF/{classes,lib}

# Copy compiled classes
cp -r build/* dist/GV/WEB-INF/classes/

# Copy configuration
cp webapp/WEB-INF/web.xml dist/GV/WEB-INF/
cp webapp/WEB-INF/classes/*.xml dist/GV/WEB-INF/classes/

# Copy libraries
cp lib/*.jar dist/GV/WEB-INF/lib/

# Copy web resources
cp webapp/*.jsp webapp/*.jpg webapp/*.png webapp/*.gif dist/GV/
cp -r webapp/css webapp/js dist/GV/

# Create WAR
cd dist/GV
jar -cvf ../GV.war *
cd ../..
```

#### 3. Deploy Manually

```bash
# Copy WAR to Tomcat
cp dist/GV.war /home/star/work/apache-tomcat-8.5.57/webapps/

# Restart Tomcat
/home/star/work/apache-tomcat-8.5.57/bin/shutdown.sh
/home/star/work/apache-tomcat-8.5.57/bin/startup.sh
```

---

## Verification

### Check Deployment Status

```bash
# Check if WAR is deployed
ls -lh /home/star/work/apache-tomcat-8.5.57/webapps/GV

# Check Tomcat logs for errors
tail -100 /home/star/work/apache-tomcat-8.5.57/logs/catalina.out

# Check application-specific logs
tail -100 /home/star/work/apache-tomcat-8.5.57/logs/localhost.*.log
```

### Test the Application

1. **Access the main page:**
   ```
   http://localhost:8089/GV/input.jsp
   ```

2. **You should see:**
   - Product input form (家具构件开料明细)
   - Add row buttons
   - Board configuration options
   - Submit button (确认完成/完成开板)

3. **Test with sample data:**
   - Product Code: A001
   - Product Name: Door Panel
   - Length: 2000
   - Width: 600
   - Thickness: 18
   - Color: White Oak
   - Quantity: 4
   - Grain: Mixed (混合)

4. **Configure board:**
   - Select board size: 4 x 8 呎 (1220 x 2440)
   - Saw kerf: 3 (mm)
   - Utilization: 0.78

5. **Submit and check results:**
   - Should show cutting diagram
   - Product placement visualization
   - Material utilization statistics

---

## Troubleshooting

### Build Errors

**Problem:** `javac: command not found`
```bash
# Check Java installation
java -version
javac -version

# Set JAVA_HOME if needed
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```

**Problem:** Compilation errors
```bash
# Check classpath includes all JARs
ls -1 lib/*.jar | wc -l  # Should be 29

# Verify Tomcat servlet-api
ls /home/star/work/apache-tomcat-8.5.57/lib/servlet-api.jar
```

**Problem:** Character encoding errors
```bash
# Ensure UTF-8 encoding
export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF-8
javac -encoding UTF-8 ...
```

### Deployment Errors

**Problem:** Port already in use
```bash
# Check what's using port 8089
lsof -i :8089
netstat -tulpn | grep 8089

# Stop conflicting service or change Tomcat port
vim /home/star/work/apache-tomcat-8.5.57/conf/server.xml
```

**Problem:** Tomcat not starting
```bash
# Check Tomcat logs
cat /home/star/work/apache-tomcat-8.5.57/logs/catalina.out

# Check permissions
ls -l /home/star/work/apache-tomcat-8.5.57/bin/*.sh

# Make scripts executable
chmod +x /home/star/work/apache-tomcat-8.5.57/bin/*.sh
```

**Problem:** Application not deploying
```bash
# Check webapps directory
ls -l /home/star/work/apache-tomcat-8.5.57/webapps/

# Check for deployment errors
grep -i "error\|exception" /home/star/work/apache-tomcat-8.5.57/logs/catalina.out | tail -20

# Verify WAR file
jar -tf dist/GV.war | head -20
```

### Runtime Errors

**Problem:** 404 Not Found
```bash
# Verify correct URL format
# Correct: http://localhost:8089/GV/input.jsp
# Wrong:   http://localhost:8080/GV/input.jsp (wrong port)

# Check server.xml for port
grep 'Connector port' /home/star/work/apache-tomcat-8.5.57/conf/server.xml
```

**Problem:** 500 Internal Server Error
```bash
# Check application logs
tail -100 /home/star/work/apache-tomcat-8.5.57/logs/catalina.out

# Check for missing dependencies
ls /home/star/work/apache-tomcat-8.5.57/webapps/GV/WEB-INF/lib/ | wc -l
```

**Problem:** Blank page or no response
```bash
# Check if action is mapped correctly
cat /home/star/work/apache-tomcat-8.5.57/webapps/GV/WEB-INF/classes/struts.xml

# Test direct action URL
curl http://localhost:8089/GV/createView.action
```

---

## Configuration

### Changing Tomcat Port

Edit `/home/star/work/apache-tomcat-8.5.57/conf/server.xml`:

```xml
<!-- Change from 8089 to your desired port -->
<Connector port="8089" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
```

Restart Tomcat after changes.

### Changing Application Context

To deploy at root context (`http://localhost:8089/` instead of `http://localhost:8089/GV/`):

```bash
# Rename WAR file
mv dist/GV.war dist/ROOT.war

# Deploy
cp dist/ROOT.war /home/star/work/apache-tomcat-8.5.57/webapps/
```

### Adjusting Memory Settings

For large cutting plans, increase Tomcat memory:

Edit `/home/star/work/apache-tomcat-8.5.57/bin/setenv.sh`:

```bash
export CATALINA_OPTS="-Xms512m -Xmx1024m -XX:MaxPermSize=256m"
```

---

## Development Workflow

### Making Code Changes

```bash
# 1. Edit source files
vim src/com/gv/service/ViewServiceR2.java

# 2. Rebuild
./build.sh

# 3. Redeploy
./deploy.sh

# 4. Restart Tomcat (if needed)
/home/star/work/apache-tomcat-8.5.57/bin/shutdown.sh
/home/star/work/apache-tomcat-8.5.57/bin/startup.sh
```

### Hot Reload (Development Mode)

For rapid development, deploy as exploded directory:

```bash
# Build without WAR packaging
./build.sh

# Copy exploded directory
rm -rf /home/star/work/apache-tomcat-8.5.57/webapps/GV
cp -r dist/GV /home/star/work/apache-tomcat-8.5.57/webapps/

# Enable auto-reload in context.xml
echo '<Context reloadable="true" />' > /home/star/work/apache-tomcat-8.5.57/webapps/GV/META-INF/context.xml
```

---

## Port Configuration Reference

Based on your Tomcat `server.xml`:

- **Service "Catalina"** (Port 8088) - For xiaoyaoji app
- **Service "Catalina2"** (Port 8089) - For ERP/DataCenter/GV apps

Use port **8089** for accessing GV application.

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `./build.sh` | Build application |
| `./deploy.sh` | Deploy to Tomcat |
| `bin/startup.sh` | Start Tomcat |
| `bin/shutdown.sh` | Stop Tomcat |
| `tail -f logs/catalina.out` | View logs |
| `http://localhost:8089/GV/input.jsp` | Access app |

---

## Next Steps

After successful deployment:

1. ✓ Test basic functionality with sample data
2. ✓ Review algorithm parameters in `ViewServiceR2.java`
3. ✓ Customize board sizes in `Constant.java` if needed
4. ✓ Consider upgrading Struts 2.3.x (security vulnerabilities)
5. ✓ Add unit tests for critical logic
6. ✓ Configure logging levels in `log4j.xml`

---

## Support

- **Documentation:** See `README.md` for detailed technical documentation
- **Recovery Details:** See `RECOVERY_SUMMARY.txt`
- **Logs:** Check `${TOMCAT_HOME}/logs/` directory
- **Configuration:** Review `webapp/WEB-INF/` files

---

**Last Updated:** 2025-11-08
