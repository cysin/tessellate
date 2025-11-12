# How to Run the GV Application

## TL;DR - Quick Start

```bash
cd /home/star/work/apache-tomcat-8.5.57/GV-recovered-source
./deploy-precompiled.sh
```

Then access: **http://localhost:8089/GV/input.jsp**

---

## Important Note About Compilation

The decompiled source code has some **generic type information loss** due to Java's type erasure during compilation. This causes compilation errors in some service files.

### Solution: Use Pre-compiled Classes

We provide `deploy-precompiled.sh` which uses the **original working `.class` files** from the deployed application. These files work perfectly and are production-tested.

- ✅ **Recommended**: `./deploy-precompiled.sh` (uses pre-compiled classes)
- ❌ **Not working**: `./build.sh` (recompilation has errors)

The source code is still valuable for:
- Understanding the algorithm logic
- Reviewing business rules
- Documentation purposes
- Making small modifications (if you fix the type issues)

---

## Step-by-Step Deployment

### 1. Navigate to Project Directory

```bash
cd /home/star/work/apache-tomcat-8.5.57/GV-recovered-source
```

### 2. Run Deployment Script

```bash
./deploy-precompiled.sh
```

**Expected output:**
```
[1/4] Cleaning previous build...
[2/4] Creating WAR structure...
   ✓ WAR structure created
[3/4] Creating WAR file...
   ✓ WAR file created: GV.war (8.0M)
[4/4] Deploying to Tomcat...
   ✓ Deployed to: /home/star/work/apache-tomcat-8.5.57/webapps/
```

### 3. Start/Restart Tomcat

If Tomcat is not running:
```bash
/home/star/work/apache-tomcat-8.5.57/bin/startup.sh
```

If you need to restart:
```bash
/home/star/work/apache-tomcat-8.5.57/bin/shutdown.sh
/home/star/work/apache-tomcat-8.5.57/bin/startup.sh
```

### 4. Wait for Deployment

Tomcat will automatically extract and deploy the WAR file. This takes 5-10 seconds.

Watch the deployment:
```bash
tail -f /home/star/work/apache-tomcat-8.5.57/logs/catalina.out
```

Look for:
```
INFO: Deployment of web application directory [.../webapps/GV] has finished in [XXX] ms
```

### 5. Access the Application

Open your browser:
```
http://localhost:8089/GV/input.jsp
```

**Port Notes:**
- Port **8089** is for service "Catalina2" (default for this installation)
- Port **8088** is for service "Catalina" (xiaoyaoji app)
- Check `/home/star/work/apache-tomcat-8.5.57/conf/server.xml` if neither works

---

## Using the Application

### Test with Sample Data

1. **Enter Product Information:**
   - Product Code: `A001`
   - Product Name: `Cabinet Door`
   - Length (长): `2000` mm
   - Width (宽): `600` mm
   - Thickness (厚): `18` mm
   - Color (花色): `White Oak`
   - Quantity (数量): `4`
   - Grain Direction (纹理): Select `混合 (Mixed)` or `单向 (Directional)`

2. **Add More Products:**
   - Click the "添加" (Add) button to add more rows
   - Add variety: different sizes, quantities

3. **Configure Board Settings:**
   - Board Size (板材规格): Select `4 x 8 呎 (1220 x 2440)`
   - Saw Kerf (裁切锯口尺寸): `3` mm
   - Utilization Rate (板材利用率): `0.78` (78%)

4. **Optional - Add Leftover Material:**
   - Check the box: `库存余料优先` (Prioritize leftover material)
   - Add leftover dimensions if you have them

5. **Generate Cutting Plan:**
   - Click: `确认完成` (Confirm) button
   - Then click: `确认开板` (Generate cutting plan)

6. **View Results:**
   - Visual cutting diagram showing product placement
   - Product list with quantities
   - Leftover material summary
   - Material utilization statistics

7. **Print (Optional):**
   - Click the print button to generate printable cutting instructions

---

## Troubleshooting

### Problem: Port 8089 not responding

**Solution:**
```bash
# Check which port Tomcat is using
grep 'Connector port' /home/star/work/apache-tomcat-8.5.57/conf/server.xml

# Try the alternate port
http://localhost:8088/GV/input.jsp
```

### Problem: 404 Not Found

**Solution:**
```bash
# Check if application is deployed
ls -l /home/star/work/apache-tomcat-8.5.57/webapps/GV

# If directory doesn't exist, redeploy
cd /home/star/work/apache-tomcat-8.5.57/GV-recovered-source
./deploy-precompiled.sh

# Restart Tomcat
/home/star/work/apache-tomcat-8.5.57/bin/shutdown.sh
/home/star/work/apache-tomcat-8.5.57/bin/startup.sh
```

### Problem: Blank page or errors

**Solution:**
```bash
# Check Tomcat logs for errors
tail -100 /home/star/work/apache-tomcat-8.5.57/logs/catalina.out

# Look for exceptions or error messages
grep -i "error\|exception" /home/star/work/apache-tomcat-8.5.57/logs/catalina.out | tail -20
```

### Problem: Application not processing requests

**Solution:**
```bash
# Test the action endpoint directly
curl http://localhost:8089/GV/createView.action

# If this returns an error, check struts configuration
cat /home/star/work/apache-tomcat-8.5.57/webapps/GV/WEB-INF/classes/struts.xml
```

### Problem: Want to modify and recompile

The decompiled code has generic type issues. To fix:

1. **Option A:** Manually fix type declarations in `ViewServiceR2.java`:
   ```java
   // Change from:
   for (List list : vt) {
   // To:
   for (List<Material> list : vt) {
   ```

2. **Option B:** Use a different decompiler (e.g., JD-GUI, Procyon)

3. **Option C:** Work with the `.class` files directly using tools like:
   - Java Agent for runtime modification
   - Bytecode manipulation libraries (ASM, Javassist)

---

## File Structure After Deployment

```
GV-recovered-source/
├── deploy-precompiled.sh      ← Use this to deploy
├── build.sh                    (Has compilation issues)
├── deploy.sh                   (Requires build.sh to work first)
├── dist/
│   └── GV.war                  (8.0M - Deployable WAR file)
├── src/                        (Decompiled source - for reference)
├── webapp/                     (Web resources)
├── lib/                        (Dependencies - 29 JAR files)
├── README.md                   (Technical documentation)
├── QUICKSTART.md               (Detailed setup guide)
├── RECOVERY_SUMMARY.txt        (Recovery details)
└── HOWTO_RUN.md               (This file)
```

---

## Deployment Verification Checklist

- [ ] Script executed without errors
- [ ] WAR file created: `dist/GV.war` (should be ~8MB)
- [ ] WAR copied to: `/home/star/work/apache-tomcat-8.5.57/webapps/GV.war`
- [ ] Tomcat is running (check with: `ps aux | grep catalina`)
- [ ] WAR automatically extracted to: `webapps/GV/` directory
- [ ] No errors in: `logs/catalina.out`
- [ ] Application accessible at: `http://localhost:8089/GV/input.jsp`

---

## Advanced Configuration

### Change Application Port

Edit: `/home/star/work/apache-tomcat-8.5.57/conf/server.xml`

```xml
<Connector port="8089" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
```

Restart Tomcat after changes.

### Increase Memory for Large Cutting Plans

Create: `/home/star/work/apache-tomcat-8.5.57/bin/setenv.sh`

```bash
#!/bin/bash
export CATALINA_OPTS="-Xms512m -Xmx2048m -XX:MaxPermSize=512m"
```

Make executable:
```bash
chmod +x /home/star/work/apache-tomcat-8.5.57/bin/setenv.sh
```

### Enable Debug Logging

Edit: `webapps/GV/WEB-INF/classes/log4j.xml`

Change level to DEBUG:
```xml
<logger name="com.gv">
    <level value="DEBUG"/>
</logger>
```

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Struts 2.3.x Vulnerabilities:**
   - This application uses Struts 2.3.1.2
   - Known security vulnerabilities exist
   - **Do not expose to public internet**
   - Use only in trusted internal networks

2. **Recommended Actions:**
   - Run behind a firewall
   - Use VPN for remote access
   - Consider upgrading to Struts 2.5+ (requires code changes)
   - Implement authentication if needed

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Deploy app | `cd GV-recovered-source && ./deploy-precompiled.sh` |
| Start Tomcat | `/home/star/work/apache-tomcat-8.5.57/bin/startup.sh` |
| Stop Tomcat | `/home/star/work/apache-tomcat-8.5.57/bin/shutdown.sh` |
| View logs | `tail -f /home/star/work/apache-tomcat-8.5.57/logs/catalina.out` |
| Check deployment | `ls -l /home/star/work/apache-tomcat-8.5.57/webapps/GV` |
| Access app | Open `http://localhost:8089/GV/input.jsp` |
| Test action | `curl http://localhost:8089/GV/createView.action` |

---

## Getting Help

- **Technical Documentation:** See `README.md`
- **Quick Start Guide:** See `QUICKSTART.md`
- **Recovery Details:** See `RECOVERY_SUMMARY.txt`
- **Source Code:** Browse `src/com/gv/`
- **Tomcat Logs:** Check `/home/star/work/apache-tomcat-8.5.57/logs/`

---

## Summary

The GV application is now ready to run:

1. ✅ Source code recovered and documented
2. ✅ Dependencies included (29 JAR files)
3. ✅ Deployment script created and tested
4. ✅ WAR file generated (8.0M)
5. ✅ Ready to deploy to Tomcat

**Next step:** Run `./deploy-precompiled.sh` and access the application!

---

**Last Updated:** 2025-11-08
