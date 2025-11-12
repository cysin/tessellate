#!/bin/bash
################################################################################
# GV Application Deployment Script
################################################################################

set -e  # Exit on error

echo "=========================================="
echo "GV Application Deployment Script"
echo "=========================================="

# Configuration
APP_NAME="GV"
WAR_FILE="dist/$APP_NAME.war"
TOMCAT_HOME="/home/star/work/apache-tomcat-8.5.57"
WEBAPPS_DIR="$TOMCAT_HOME/webapps"

# Check if WAR exists
if [ ! -f "$WAR_FILE" ]; then
    echo "ERROR: WAR file not found: $WAR_FILE"
    echo "Please run ./build.sh first"
    exit 1
fi

echo ""
echo "[1/4] Checking Tomcat installation..."
if [ ! -d "$TOMCAT_HOME" ]; then
    echo "ERROR: Tomcat not found at: $TOMCAT_HOME"
    echo "Please update TOMCAT_HOME in this script"
    exit 1
fi
echo "   ✓ Found Tomcat at: $TOMCAT_HOME"

# Backup existing deployment
echo ""
echo "[2/4] Checking for existing deployment..."
if [ -d "$WEBAPPS_DIR/$APP_NAME" ] || [ -f "$WEBAPPS_DIR/$APP_NAME.war" ]; then
    BACKUP_DIR="$WEBAPPS_DIR/${APP_NAME}_backup_$(date +%Y%m%d_%H%M%S)"
    echo "   Found existing deployment, creating backup..."
    echo "   Backup location: $BACKUP_DIR"

    mkdir -p "$BACKUP_DIR"
    [ -d "$WEBAPPS_DIR/$APP_NAME" ] && mv "$WEBAPPS_DIR/$APP_NAME" "$BACKUP_DIR/"
    [ -f "$WEBAPPS_DIR/$APP_NAME.war" ] && mv "$WEBAPPS_DIR/$APP_NAME.war" "$BACKUP_DIR/"

    echo "   ✓ Backup created"
else
    echo "   No existing deployment found"
fi

# Deploy WAR
echo ""
echo "[3/4] Deploying application..."
cp "$WAR_FILE" "$WEBAPPS_DIR/"
echo "   ✓ WAR file copied to: $WEBAPPS_DIR/$APP_NAME.war"

# Check Tomcat status
echo ""
echo "[4/4] Checking Tomcat status..."
CATALINA_PID=$(ps aux | grep catalina | grep -v grep | awk '{print $2}' | head -1)
if [ -n "$CATALINA_PID" ]; then
    echo "   Tomcat is running (PID: $CATALINA_PID)"
    echo "   Application will be auto-deployed in a few seconds..."
    echo ""
    echo "   Watching deployment..."
    sleep 3

    if [ -d "$WEBAPPS_DIR/$APP_NAME" ]; then
        echo "   ✓ Application deployed successfully!"
    else
        echo "   Waiting for deployment..."
        sleep 5
        if [ -d "$WEBAPPS_DIR/$APP_NAME" ]; then
            echo "   ✓ Application deployed successfully!"
        else
            echo "   Application is deploying (check Tomcat logs)"
        fi
    fi
else
    echo "   Tomcat is not running"
    echo "   Please start Tomcat to deploy the application:"
    echo "   cd $TOMCAT_HOME && ./bin/startup.sh"
fi

# Summary
echo ""
echo "=========================================="
echo "Deployment Summary"
echo "=========================================="
echo "Application:  $APP_NAME"
echo "WAR file:     $WEBAPPS_DIR/$APP_NAME.war"
echo "Deploy path:  $WEBAPPS_DIR/$APP_NAME/"
echo ""
echo "Access URLs:"
echo "  http://localhost:8089/$APP_NAME/input.jsp"
echo "  http://localhost:8089/$APP_NAME/"
echo ""
echo "Useful commands:"
echo "  View logs:    tail -f $TOMCAT_HOME/logs/catalina.out"
echo "  Stop Tomcat:  $TOMCAT_HOME/bin/shutdown.sh"
echo "  Start Tomcat: $TOMCAT_HOME/bin/startup.sh"
echo ""
