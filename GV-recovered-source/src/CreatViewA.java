/*
 * Decompiled with CFR 0.152.
 */
import com.gv.model.Material;
import com.gv.model.Product;
import java.util.ArrayList;
import java.util.List;

public class CreatViewA {
    public static void main(String[] arg) {
        ArrayList<Material> materials = new ArrayList<Material>();
        List<Material> m_materials = ProAndMat.createMaterials();
        List<Product> m_products = ProAndMat.createProducts();
        Product product = null;
        Material m_material = null;
        double w_c_mod = 0.0;
        double h_c_mod = 0.0;
        double m_mod = 0.0;
        boolean c_type = false;
        int p_count = 0;
        int m_m_no = 0;
        int m_p_no = 0;
        while (m_products.size() > 0) {
            int i;
            Product p;
            Material material = new Material();
            m_m_no = 0;
            m_p_no = 0;
            m_mod = 2000.0;
            p_count = 0;
            int i2 = 0;
            while (i2 < m_materials.size()) {
                m_material = m_materials.get(i2);
                int j = 0;
                while (j < m_products.size()) {
                    p = m_products.get(j);
                    if (!(m_material.getR_height() < p.getP_height()) && !(m_material.getR_width() < p.getP_width())) {
                        w_c_mod = m_material.getR_width() % p.getP_width();
                        h_c_mod = m_material.getR_height() % p.getP_height();
                        if (0.0 == w_c_mod && m_material.getR_width() / p.getP_width() >= 1.0) {
                            m_mod = w_c_mod;
                            p_count = (int)(m_material.getR_width() / p.getP_width());
                            c_type = false;
                            m_p_no = j;
                            m_m_no = i2;
                            break;
                        }
                        if (0.0 == h_c_mod && m_material.getR_height() / p.getP_height() >= 1.0) {
                            m_mod = h_c_mod;
                            p_count = (int)(m_material.getR_height() / p.getP_height());
                            c_type = true;
                            m_p_no = j;
                            m_m_no = i2;
                            break;
                        }
                        if (w_c_mod >= 0.0 && m_mod >= w_c_mod) {
                            m_mod = w_c_mod;
                            p_count = (int)(m_material.getR_width() / p.getP_width());
                            c_type = false;
                            m_p_no = j;
                            m_m_no = i2;
                        }
                        if (h_c_mod >= 0.0 && m_mod >= h_c_mod) {
                            m_mod = h_c_mod;
                            p_count = (int)(m_material.getR_height() / p.getP_height());
                            c_type = true;
                            m_p_no = j;
                            m_m_no = i2;
                        }
                    }
                    ++j;
                }
                ++i2;
            }
            System.out.println("\ufffd\ufffd\u01b7\ufffd\ufffd\ufffd\ufffd" + p_count);
            if (p_count == 0) {
                System.out.println("\u052d\ufffd\u03f2\ufffd\ufffd\ufffd");
                break;
            }
            material.setM_name(m_materials.get(m_m_no).getM_name());
            material.setM_count(m_materials.get(m_m_no).getM_count());
            material.setM_height(m_materials.get(m_m_no).getM_height());
            material.setM_color(m_materials.get(m_m_no).getM_color());
            material.setM_products(m_materials.get(m_m_no).getM_products());
            material.setM_width(m_materials.get(m_m_no).getM_width());
            material.setR_height(m_materials.get(m_m_no).getR_height());
            material.setR_width(m_materials.get(m_m_no).getR_width());
            if (1.0 == material.getM_count()) {
                System.out.println("\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd");
                m_materials.remove(m_m_no);
            } else {
                m_materials.get(m_m_no).setM_count(material.getM_count() - 1.0);
            }
            try {
                product = m_products.get(m_p_no);
                System.out.println("\ufffd\ufffd\ufffd\ufffd\ufffd" + m_m_no);
                System.out.println("\ufffd\ufffd\ufffd\u01b7" + m_p_no);
            }
            catch (Exception e) {
                System.out.println("\ufffd\ucce3" + m_p_no);
                System.out.println("\ufffd\ufffd\u6cbb\ufffd\ufffd");
                break;
            }
            ArrayList<Product> m_ps = new ArrayList<Product>();
            if (!c_type) {
                i = 0;
                while (i < p_count) {
                    p = new Product();
                    p.setM_left(material.getM_width() - material.getR_width() + (double)i * product.getP_width());
                    p.setM_top(material.getM_height() - material.getR_height());
                    p.setP_name(product.getP_name());
                    m_ps.add(p);
                    p = null;
                    ++i;
                }
                material.setR_height(material.getR_height() - product.getP_height());
            }
            if (c_type) {
                i = 0;
                while (i < p_count) {
                    p = new Product();
                    p.setM_left(material.getM_width() - material.getR_width());
                    p.setM_top(material.getM_height() - material.getR_height() + (double)i * product.getP_height());
                    p.setP_name(product.getP_name());
                    m_ps.add(p);
                    p = null;
                    ++i;
                }
                material.setR_width(material.getR_width() - product.getP_width());
            }
            if (material.getM_products() == null) {
                System.out.println("\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\u04bb\ufffd\ufffd\ufffd");
                material.setM_products(m_ps);
                material.setM_count(1.0);
                m_materials.add(material);
                System.out.println(m_materials.size());
            } else {
                System.out.println("\ufffd\u00f5\ufffd\ufffd\u03f2\ufffd\ufffd\ufffd");
                List<Product> temp_ps = material.getM_products();
                temp_ps.addAll(m_ps);
                material.setM_products(temp_ps);
                for (Material m : materials) {
                    if (!m.getM_name().equals(material.getM_name()) || m.getR_height() != material.getR_height() + product.getP_height() || m.getR_width() != material.getR_width() + product.getP_width()) continue;
                    materials.remove(m);
                }
            }
            if ((double)p_count < product.getP_count()) {
                m_products.get(m_p_no).setP_count(product.getP_count() - (double)p_count);
            } else {
                System.out.println("\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd" + m_p_no);
                m_products.remove(m_p_no);
            }
            materials.add(material);
            material = null;
            System.out.println("---------------");
        }
        System.out.println(m_materials.size());
    }
}
