/*
 * Decompiled with CFR 0.152.
 */
package com.gv.tool;

import com.gv.model.Material;
import com.gv.model.Product;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.List;

public class CommonTools {
    public static Material cloneScheme(Material src) throws RuntimeException {
        ByteArrayOutputStream memoryBuffer = new ByteArrayOutputStream();
        ObjectOutputStream out = null;
        ObjectInputStream in = null;
        Material dist = null;
        try {
            try {
                out = new ObjectOutputStream(memoryBuffer);
                out.writeObject(src);
                out.flush();
                in = new ObjectInputStream(new ByteArrayInputStream(memoryBuffer.toByteArray()));
                dist = (Material)in.readObject();
            }
            catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
        finally {
            if (out != null) {
                try {
                    out.close();
                    out = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            if (in != null) {
                try {
                    in.close();
                    in = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        return dist;
    }

    public static Product clonePro(Product src) throws RuntimeException {
        ByteArrayOutputStream memoryBuffer = new ByteArrayOutputStream();
        ObjectOutputStream out = null;
        ObjectInputStream in = null;
        Product dist = null;
        try {
            try {
                out = new ObjectOutputStream(memoryBuffer);
                out.writeObject(src);
                out.flush();
                in = new ObjectInputStream(new ByteArrayInputStream(memoryBuffer.toByteArray()));
                dist = (Product)in.readObject();
            }
            catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
        finally {
            if (out != null) {
                try {
                    out.close();
                    out = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            if (in != null) {
                try {
                    in.close();
                    in = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        return dist;
    }

    public static List<Product> cloneProList(List<Product> src) throws RuntimeException {
        ByteArrayOutputStream memoryBuffer = new ByteArrayOutputStream();
        ObjectOutputStream out = null;
        ObjectInputStream in = null;
        List dist = null;
        try {
            try {
                out = new ObjectOutputStream(memoryBuffer);
                out.writeObject(src);
                out.flush();
                in = new ObjectInputStream(new ByteArrayInputStream(memoryBuffer.toByteArray()));
                dist = (List)in.readObject();
            }
            catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
        finally {
            if (out != null) {
                try {
                    out.close();
                    out = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            if (in != null) {
                try {
                    in.close();
                    in = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        return dist;
    }

    public static List<Material> cloneMatList(List<Material> src) throws RuntimeException {
        ByteArrayOutputStream memoryBuffer = new ByteArrayOutputStream();
        ObjectOutputStream out = null;
        ObjectInputStream in = null;
        List dist = null;
        try {
            try {
                out = new ObjectOutputStream(memoryBuffer);
                out.writeObject(src);
                out.flush();
                in = new ObjectInputStream(new ByteArrayInputStream(memoryBuffer.toByteArray()));
                dist = (List)in.readObject();
            }
            catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
        finally {
            if (out != null) {
                try {
                    out.close();
                    out = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            if (in != null) {
                try {
                    in.close();
                    in = null;
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }
        return dist;
    }
}
