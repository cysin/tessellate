/*
 * Decompiled with CFR 0.152.
 */
import com.gv.model.Material;
import com.gv.model.Product;
import java.util.ArrayList;
import java.util.List;

public final class ProAndMat {
    public static List<Material> createMaterials() {
        ArrayList<Material> m_materials = new ArrayList<Material>();
        Material m = new Material();
        m.setM_width(1530.0);
        m.setM_height(3060.0);
        m.setR_width(1530.0);
        m.setR_height(3060.0);
        m.setM_name("5*10");
        m.setM_count(2.0);
        m_materials.add(m);
        m = null;
        m = new Material();
        m.setM_width(1530.0);
        m.setM_height(2440.0);
        m.setR_width(1530.0);
        m.setR_height(2440.0);
        m.setM_name("5*10");
        m.setM_count(2.0);
        m_materials.add(m);
        m = null;
        m = new Material();
        m.setM_width(1220.0);
        m.setM_height(2440.0);
        m.setR_width(1220.0);
        m.setR_height(2440.0);
        m.setM_name("4*8");
        m.setM_count(5.0);
        m_materials.add(m);
        m = null;
        m = new Material();
        m.setM_width(1220.0);
        m.setM_height(2750.0);
        m.setR_width(1220.0);
        m.setR_height(2750.0);
        m.setM_name("4*8");
        m.setM_count(5.0);
        m_materials.add(m);
        m = null;
        m = new Material();
        m.setM_width(1220.0);
        m.setM_height(3060.0);
        m.setR_width(1220.0);
        m.setR_height(3060.0);
        m.setM_name("4*10");
        m.setM_count(3.0);
        m_materials.add(m);
        m = null;
        m = new Material();
        m.setM_width(1530.0);
        m.setM_height(2750.0);
        m.setR_width(1530.0);
        m.setR_height(2750.0);
        m.setM_name("5*9");
        m.setM_count(3.0);
        m_materials.add(m);
        m = null;
        return m_materials;
    }

    public static List<Product> createProducts() {
        ArrayList<Product> m_products = new ArrayList<Product>();
        Product p = new Product();
        p.setP_width(125.0);
        p.setP_height(2403.0);
        p.setP_name("\ufffd\u06b2\ufffd\ufffd1");
        p.setP_count(20.0);
        m_products.add(p);
        p = null;
        p = new Product();
        p.setP_width(115.0);
        p.setP_height(1987.0);
        p.setP_name("\ufffd\u06b2\ufffd\ufffd2");
        p.setP_count(10.0);
        m_products.add(p);
        p = null;
        p = new Product();
        p.setP_width(105.0);
        p.setP_height(2019.0);
        p.setP_name("\ufffd\u06b2\ufffd\ufffd3");
        p.setP_count(15.0);
        m_products.add(p);
        p = null;
        p = new Product();
        p.setP_width(99.0);
        p.setP_height(2051.0);
        p.setP_name("\ufffd\u06b2\ufffd\ufffd4");
        p.setP_count(15.0);
        m_products.add(p);
        p = null;
        p = new Product();
        p.setP_width(85.0);
        p.setP_height(2083.0);
        p.setP_name("\ufffd\u06b2\ufffd\ufffd5");
        p.setP_count(20.0);
        m_products.add(p);
        p = null;
        return m_products;
    }
}
