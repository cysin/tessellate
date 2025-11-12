/*
 * Decompiled with CFR 0.152.
 */
import com.gv.model.Material;
import com.gv.model.Product;
import java.util.ArrayList;
import java.util.List;

public class CreatTest {
    public static void main(String[] args) {
        ArrayList<Material> materials = new ArrayList<Material>();
        List<Material> m_materials = ProAndMat.createMaterials();
        List<Product> m_products = ProAndMat.createProducts();
        Material material = null;
        Product product = null;
        Material m_material = null;
        double w_c_mod = 0.0;
        double h_c_mod = 0.0;
        double m_mod = 0.0;
        double c_type = 0.0;
        double p_count = 0.0;
        int m_m_no = 0;
        int m_p_no = 0;
        int temp_m_no = -1;
        int f_no = 0;
        int f_count = 0;
        while (m_products.size() > 0) {
            Product p;
            m_mod = 2000.0;
            p_count = 0.0;
            int i = 0;
            while (i < m_materials.size()) {
                m_material = m_materials.get(i);
                int j = 0;
                while (j < m_products.size()) {
                    Product p2 = m_products.get(j);
                    w_c_mod = m_material.getR_width() % p2.getP_width();
                    h_c_mod = m_material.getR_height() % p2.getP_height();
                    if (m_mod > w_c_mod && w_c_mod >= 0.0) {
                        m_mod = w_c_mod;
                        p_count = m_material.getR_width() / p2.getP_width();
                        c_type = 0.0;
                        m_p_no = j;
                        m_m_no = i;
                    }
                    if (m_mod > h_c_mod && h_c_mod >= 0.0) {
                        m_mod = h_c_mod;
                        p_count = m_material.getR_height() / p2.getP_height();
                        c_type = 1.0;
                        m_p_no = j;
                        m_m_no = i;
                    }
                    ++j;
                }
                ++i;
            }
            System.out.println("\ufffd\ufffd" + (f_count + 1) + "\ufffd\u03a3\ufffd\u052d\ufffd\u03f1\ufffd\ufffd" + m_m_no + ";\ufffd\ufffd\u01b7\ufffd\ufffd\ufffd" + m_p_no);
            if (0.0 == p_count) {
                System.out.println("\u052d\ufffd\u03f2\ufffd\ufffd\ufffd");
                break;
            }
            if (temp_m_no != m_m_no) {
                material = m_materials.get(m_m_no);
                if (0.0 == material.getM_count()) {
                    System.out.println("\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd");
                    m_materials.remove(m_m_no);
                    continue;
                }
                m_materials.get(m_m_no).setM_count(material.getM_count() - 1.0);
                System.out.println("\u0221\ufffd\u00b0\ufffd");
            }
            try {
                product = m_products.get(m_p_no);
                System.out.println("\ufffd\ufffd" + m_p_no);
            }
            catch (Exception e) {
                System.out.println("\ufffd\ucce3" + m_p_no);
                System.out.println("\ufffd\ufffd\u6cbb\ufffd\ufffd");
                break;
            }
            ArrayList<Product> m_ps = new ArrayList<Product>();
            if (0.0 == c_type) {
                double i2 = 0.0;
                while (i2 < p_count) {
                    p = new Product();
                    p.setM_left(i2 * product.getP_width());
                    p.setM_top(material.getM_height() - material.getR_height());
                    p.setP_name(product.getP_name());
                    m_ps.add(p);
                    p = null;
                    i2 += 1.0;
                }
                material.setR_height(material.getR_height() - product.getP_height());
            }
            if (1.0 == c_type) {
                double i3 = 0.0;
                while (i3 < p_count) {
                    p = new Product();
                    p.setM_left(material.getM_width() - material.getR_width());
                    p.setM_top(i3 * product.getP_height());
                    p.setP_name(product.getP_name());
                    m_ps.add(p);
                    p = null;
                    i3 += 1.0;
                }
                material.setR_width(material.getR_width() - product.getP_width());
            }
            if (material.getM_products() == null) {
                System.out.println("\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\u04bb\ufffd\ufffd\ufffd");
                material.setM_products(m_ps);
                material.setM_u_count(material.getM_u_count() + 1);
            } else {
                System.out.println("\ufffd\u00f5\ufffd\ufffd\u03f2\ufffd\ufffd\ufffd");
                List<Product> temp_ps = material.getM_products();
                temp_ps.addAll(m_ps);
                material.setM_products(temp_ps);
            }
            if (p_count < product.getP_count()) {
                m_products.get(m_p_no).setP_count(product.getP_count() - p_count);
            } else {
                System.out.println("\ufffd\u01b3\ufffd\ufffd\ufffd" + m_p_no);
                m_products.remove(m_p_no);
            }
            if (f_count == 0) {
                f_no = m_m_no;
            }
            if (temp_m_no != m_m_no) {
                System.out.println("\u04bb\ufffd\ufffd\u5d26\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd");
                materials.add(material);
                if (f_no == m_m_no) {
                    materials.remove(0);
                }
            }
            temp_m_no = m_m_no;
            ++f_count;
        }
        System.out.println(m_materials.size());
    }
}
