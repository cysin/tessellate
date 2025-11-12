/*
 * Decompiled with CFR 0.152.
 */
package com.gv.constant;

import com.gv.model.Material;
import java.util.HashMap;
import java.util.Map;

public class Constant {
    private static final Map<String, Material> material_c = Constant.initMaterial();

    private static Map<String, Material> initMaterial() {
        HashMap<String, Material> material_c = new HashMap<String, Material>();
        Material m = new Material();
        m.setM_width(1530.0);
        m.setM_height(3060.0);
        m.setM_name("5 x 10");
        material_c.put(m.getM_name(), m);
        m = null;
        m = new Material();
        m.setM_width(1530.0);
        m.setM_height(2440.0);
        m.setM_name("5 x 10");
        material_c.put(m.getM_name(), m);
        m = null;
        m = new Material();
        m.setM_width(1220.0);
        m.setM_height(2440.0);
        m.setM_name("4 x 8");
        material_c.put(m.getM_name(), m);
        m = null;
        m = new Material();
        m.setM_width(1530.0);
        m.setM_height(2440.0);
        m.setM_name("5 x 8");
        material_c.put(m.getM_name(), m);
        m = null;
        m = new Material();
        m.setM_width(1220.0);
        m.setM_height(2750.0);
        m.setM_name("4 x 9");
        material_c.put(m.getM_name(), m);
        m = null;
        m = new Material();
        m.setM_width(1220.0);
        m.setM_height(3060.0);
        m.setM_name("4 x 10");
        material_c.put(m.getM_name(), m);
        m = null;
        m = new Material();
        m.setM_width(1530.0);
        m.setM_height(2750.0);
        m.setM_name("5 x 9");
        material_c.put(m.getM_name(), m);
        m = null;
        return material_c;
    }

    public static Map<String, Material> getMaterialC() {
        return material_c;
    }
}
