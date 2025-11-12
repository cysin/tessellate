/*
 * Decompiled with CFR 0.152.
 */
package com.gv.service;

import com.gv.model.Material;
import com.gv.model.Product;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class CopyOfViewService {
    public List<Material> createView(List<Product> m_products, List<Material> m_materials, double saw_bite) {
        ArrayList<Material> materials = new ArrayList<Material>();
        Product product = null;
        Material m_material = null;
        Map<String, List<Product>> m_products_map = this.processProduct(m_products);
        Map<String, List<Material>> m_materials_map = this.processMaterial(m_materials);
        Iterator<String> it = m_products_map.keySet().iterator();
        double w_c_mod = 0.0;
        double h_c_mod = 0.0;
        double m_mod = 0.0;
        boolean c_type = false;
        int p_count = 0;
        int m_m_no = 0;
        int m_p_no = 0;
        block0: while (it.hasNext()) {
            String key = it.next();
            m_products = m_products_map.get(key);
            while (m_products.size() > 0) {
                Product p;
                Material material = new Material();
                m_m_no = 0;
                m_p_no = 0;
                Product m_h_product = CopyOfViewService.mathMinProduct(m_products, 0);
                Product m_w_product = CopyOfViewService.mathMinProduct(m_products, 1);
                m_mod = 4000.0;
                p_count = -1;
                m_materials = m_materials_map.get(key);
                if (m_materials != null) {
                    int i = 0;
                    while (i < m_materials.size()) {
                        m_material = m_materials.get(i);
                        int j = 0;
                        while (j < m_products.size()) {
                            p = m_products.get(j);
                            if (!(m_material.getR_height() < p.getP_height()) && !(m_material.getR_width() < p.getP_width())) {
                                w_c_mod = (m_material.getR_width() - saw_bite * (m_material.getR_width() / p.getP_width() - 1.0)) % p.getP_width();
                                h_c_mod = (m_material.getR_height() - saw_bite * (m_material.getR_height() / p.getP_height() - 1.0)) % p.getP_height();
                                if (0.0 == h_c_mod) {
                                    w_c_mod = m_material.getR_width() - saw_bite - p.getP_width();
                                    if (w_c_mod < m_h_product.getP_width() && w_c_mod < m_w_product.getP_width()) {
                                        m_mod = h_c_mod;
                                        p_count = (int)((m_material.getR_height() + saw_bite) / (p.getP_height() + saw_bite));
                                        c_type = true;
                                        m_p_no = j;
                                        m_m_no = i;
                                    }
                                } else if (0.0 == w_c_mod) {
                                    h_c_mod = m_material.getR_height() - saw_bite - p.getP_height();
                                    if (h_c_mod < m_h_product.getP_height() && h_c_mod < m_w_product.getP_height()) {
                                        m_mod = w_c_mod;
                                        p_count = (int)((m_material.getR_width() + saw_bite) / (p.getP_width() + saw_bite));
                                        c_type = false;
                                        m_p_no = j;
                                        m_m_no = i;
                                    }
                                } else {
                                    boolean flag = false;
                                    if (h_c_mod >= 0.0 && w_c_mod >= 0.0 && m_mod >= h_c_mod + w_c_mod) {
                                        m_mod = h_c_mod + w_c_mod;
                                        if (h_c_mod <= w_c_mod) {
                                            m_mod = h_c_mod;
                                            p_count = (int)((m_material.getR_height() + saw_bite) / (p.getP_height() + saw_bite));
                                            if (flag) {
                                                --p_count;
                                            }
                                            c_type = true;
                                            m_p_no = j;
                                            m_m_no = i;
                                        } else {
                                            m_mod = w_c_mod;
                                            p_count = (int)((m_material.getR_width() + saw_bite) / (p.getP_width() + saw_bite));
                                            if (flag) {
                                                --p_count;
                                            }
                                            c_type = false;
                                            m_p_no = j;
                                            m_m_no = i;
                                        }
                                    }
                                }
                            }
                            ++j;
                        }
                        ++i;
                    }
                } else {
                    System.out.println("1111");
                    continue block0;
                }
                if (-1 == p_count) {
                    System.out.println("222222");
                    continue block0;
                }
                material.setM_name(m_materials.get(m_m_no).getM_name());
                material.setM_count(m_materials.get(m_m_no).getM_count());
                material.setM_color(m_materials.get(m_m_no).getM_color());
                material.setM_products(m_materials.get(m_m_no).getM_products());
                material.setM_height(m_materials.get(m_m_no).getM_height());
                material.setM_width(m_materials.get(m_m_no).getM_width());
                material.setR_height(m_materials.get(m_m_no).getR_height());
                material.setR_width(m_materials.get(m_m_no).getR_width());
                material.setM_weight(m_materials.get(m_m_no).getM_weight());
                if (1.0 == material.getM_count()) {
                    System.out.println("223333");
                    m_materials.remove(m_m_no);
                } else {
                    m_materials.get(m_m_no).setM_count(material.getM_count() - 1.0);
                }
                while (material.getR_height() >= m_h_product.getP_height() && material.getR_width() >= m_h_product.getP_width() || material.getR_width() >= m_w_product.getP_width() && material.getR_height() >= m_w_product.getP_height()) {
                    if (material.getM_products() != null) {
                        m_m_no = 0;
                        m_p_no = 0;
                        m_mod = 2000.0;
                        p_count = -1;
                        int j = 0;
                        while (j < m_products.size()) {
                            Product p2 = m_products.get(j);
                            if (material.getR_width() < p2.getP_width() || material.getR_height() < p2.getP_height()) {
                                if (j == m_products.size() - 1) {
                                    if (-1 == p_count) break;
                                }
                            } else if (material.getR_width() >= p2.getP_width() + saw_bite && material.getR_height() >= p2.getP_height() + saw_bite) {
                                w_c_mod = (material.getR_width() - saw_bite * (material.getR_width() / p2.getP_width() - 1.0)) % p2.getP_width();
                                h_c_mod = (material.getR_height() - saw_bite * (material.getR_height() / p2.getP_height() - 1.0)) % p2.getP_height();
                                if (h_c_mod >= 0.0 && w_c_mod >= 0.0 && m_mod >= h_c_mod + w_c_mod) {
                                    m_mod = h_c_mod + w_c_mod;
                                    if (h_c_mod <= w_c_mod) {
                                        m_mod = h_c_mod;
                                        p_count = (int)((material.getR_height() + saw_bite) / (p2.getP_height() + saw_bite));
                                        c_type = true;
                                        m_p_no = j;
                                    } else {
                                        m_mod = w_c_mod;
                                        p_count = (int)((material.getR_width() + saw_bite) / (p2.getP_width() + saw_bite));
                                        c_type = false;
                                        m_p_no = j;
                                    }
                                }
                            }
                            ++j;
                        }
                    }
                    product = m_products.get(m_p_no);
                    ArrayList<Product> m_ps = new ArrayList<Product>();
                    if (!c_type) {
                        int i = 0;
                        while (i < p_count) {
                            p = new Product();
                            p.setM_left(material.getM_width() - 12.0 - material.getR_width() + (double)i * (product.getP_width() + saw_bite));
                            p.setM_top(material.getM_height() - 12.0 - material.getR_height());
                            p.setP_name(product.getP_name());
                            p.setP_height(product.getP_height());
                            p.setP_width(product.getP_width());
                            p.setP_is_copy(product.getP_is_copy());
                            p.setP_is_dir(product.getP_is_dir());
                            m_ps.add(p);
                            p = null;
                            ++i;
                        }
                        material.setR_height(material.getR_height() - product.getP_height() - saw_bite);
                    }
                    if (c_type) {
                        int i = 0;
                        while (i < p_count) {
                            p = new Product();
                            p.setM_left(material.getM_width() - 12.0 - material.getR_width());
                            p.setM_top(material.getM_height() - 12.0 - material.getR_height() + (double)i * (product.getP_height() + saw_bite));
                            p.setP_name(product.getP_name());
                            p.setP_height(product.getP_height());
                            p.setP_width(product.getP_width());
                            p.setP_is_copy(product.getP_is_copy());
                            p.setP_is_dir(product.getP_is_dir());
                            m_ps.add(p);
                            p = null;
                            ++i;
                        }
                        material.setR_width(material.getR_width() - product.getP_width() - saw_bite);
                    }
                    if (material.getM_products() == null) {
                        System.out.println("345345");
                        material.setM_products(m_ps);
                        material.setM_count(1.0);
                        m_materials.add(material);
                    } else {
                        System.out.println("345345345345345");
                        List<Product> temp_ps = material.getM_products();
                        temp_ps.addAll(m_ps);
                        material.setM_products(temp_ps);
                    }
                    if ((double)p_count < product.getP_count()) {
                        System.out.println("222222" + p_count);
                        m_products.get(m_p_no).setP_count(product.getP_count() - (double)p_count);
                        if (product.getP_is_dir() == 0) {
                            int i = 0;
                            while (i < m_products.size()) {
                                if (product.getP_is_copy() == 0) {
                                    if (product.getP_name().equals(m_products.get(i).getP_name()) && product != m_products.get(i) && product.getP_height() == m_products.get(i).getP_width() && product.getP_width() == m_products.get(i).getP_height() && 1 == m_products.get(i).getP_is_copy()) {
                                        m_products.get(i).setP_count(m_products.get(i).getP_count() - (double)p_count);
                                        System.out.println("\u751f\u4ea7\u4e86" + m_products.get(i).getP_count());
                                    }
                                } else if (product.getP_name().equals(m_products.get(i).getP_name()) && product != m_products.get(i) && product.getP_height() == m_products.get(i).getP_width() && product.getP_width() == m_products.get(i).getP_height() && m_products.get(i).getP_is_copy() == 0) {
                                    m_products.get(i).setP_count(m_products.get(i).getP_count() - (double)p_count);
                                    System.out.println("\u751f\u4ea7\u4e86" + m_products.get(i).getP_count());
                                }
                                ++i;
                            }
                        }
                        System.out.println("66666" + m_products.get(m_p_no).getP_count());
                        continue;
                    }
                    System.out.println("\u751f\u4ea7\u5b8c\u6210\u4e86" + m_p_no);
                    m_products.remove(m_p_no);
                    if (product.getP_is_dir() == 0) {
                        int i = 0;
                        while (i < m_products.size()) {
                            if (product.getP_is_copy() == 0) {
                                if (product.getP_name().equals(m_products.get(i).getP_name()) && product != m_products.get(i) && product.getP_height() == m_products.get(i).getP_width() && product.getP_width() == m_products.get(i).getP_height() && 1 == m_products.get(i).getP_is_copy()) {
                                    System.out.println("\u751f\u4ea7\u5b8c\u6210\u4e86");
                                    m_products.remove(i);
                                }
                            } else if (product.getP_name().equals(m_products.get(i).getP_name()) && product != m_products.get(i) && product.getP_height() == m_products.get(i).getP_width() && product.getP_width() == m_products.get(i).getP_height() && m_products.get(i).getP_is_copy() == 0) {
                                System.out.println("\u751f\u4ea7\u5b8c\u6210\u4e86");
                                m_products.remove(i);
                            }
                            ++i;
                        }
                    }
                    m_h_product = CopyOfViewService.mathMinProduct(m_products, 0);
                    m_w_product = CopyOfViewService.mathMinProduct(m_products, 1);
                    if (m_products.size() != 0) continue;
                    System.out.println("\ufffd\ufffd\u01b7\u022b\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd");
                    break;
                }
                materials.add(material);
                material = null;
                System.out.println("---------------");
            }
        }
        for (Material u_m : materials) {
            int i = 0;
            while (i < materials.size()) {
                if (u_m.getM_is_show() == 0 && ((Material)materials.get(i)).getM_is_show() == 0 && u_m != materials.get(i) && u_m.getM_name().equals(((Material)materials.get(i)).getM_name()) && u_m.getR_height() == ((Material)materials.get(i)).getR_height() && ((Material)materials.get(i)).getR_width() == u_m.getR_width() && ((Material)materials.get(i)).getM_color().equals(u_m.getM_color()) && ((Material)materials.get(i)).getM_weight() == u_m.getM_weight() && ((Material)materials.get(i)).getM_products().size() == u_m.getM_products().size()) {
                    List<Product> u_m_products = u_m.getM_products();
                    List<Product> m_t_products = ((Material)materials.get(i)).getM_products();
                    int flag = 0;
                    int j = 0;
                    while (j < u_m_products.size()) {
                        if (!u_m_products.get(j).getP_name().equals(m_t_products.get(j).getP_name()) || u_m_products.get(j).getM_left() != m_t_products.get(j).getM_left() || u_m_products.get(j).getM_top() != m_t_products.get(j).getM_top() || u_m_products.get(j).getP_width() != m_t_products.get(j).getP_width() || u_m_products.get(j).getP_height() != m_t_products.get(j).getP_height()) break;
                        ++flag;
                        ++j;
                    }
                    if (flag == u_m_products.size()) {
                        u_m.setM_u_count(u_m.getM_u_count() + 1);
                        ((Material)materials.get(i)).setM_is_show(1);
                    }
                }
                ++i;
            }
        }
        return materials;
    }

    private static Product mathMinProduct(List<Product> products, int min_type) {
        Product product;
        block5: {
            int min_width;
            block4: {
                product = null;
                int min_height = -1;
                min_width = -1;
                if (min_type != 0) break block4;
                for (Product p : products) {
                    if (-1 == min_height) {
                        product = p;
                        min_height = 0;
                        continue;
                    }
                    if (!(product.getP_height() > p.getP_height())) continue;
                    product = p;
                }
                break block5;
            }
            if (1 != min_type) break block5;
            for (Product p : products) {
                if (-1 == min_width) {
                    product = p;
                    min_width = 0;
                    continue;
                }
                if (!(product.getP_width() > p.getP_width())) continue;
                product = p;
            }
        }
        return product;
    }

    public Map<String, List<Material>> processMaterial(List<Material> m_materials) {
        HashMap<String, List<Material>> m_materials_map = new HashMap<String, List<Material>>();
        System.out.println("\u539f\u6599\u5206\u7ec4\u5f00\u59cb");
        int i = 0;
        while (i < m_materials.size()) {
            Material material = m_materials.get(i);
            if (material.getM_is_show() == 0) {
                ArrayList<Material> t_materials = new ArrayList<Material>();
                t_materials.add(material);
                int j = i + 1;
                while (j < m_materials.size()) {
                    if (m_materials.get(j).getM_is_show() == 0 && material.getM_weight() == m_materials.get(j).getM_weight() && material.getM_color().equals(m_materials.get(j).getM_color())) {
                        t_materials.add(m_materials.get(j));
                        m_materials.get(j).setM_is_show(1);
                    }
                    ++j;
                }
                m_materials_map.put(String.valueOf(material.getM_weight()) + "*" + material.getM_color(), t_materials);
                material = null;
                t_materials = null;
            }
            ++i;
        }
        System.out.println("\u539f\u6599\u5206\u7ec4\u7ed3\u675f");
        return m_materials_map;
    }

    public Map<String, List<Product>> processProduct(List<Product> m_products) {
        HashMap<String, List<Product>> m_products_map = new HashMap<String, List<Product>>();
        System.out.println("\u4ea7\u54c1\u5206\u7ec4\u5f00\u59cb");
        int i = 0;
        while (i < m_products.size()) {
            Product product = m_products.get(i);
            if (product.getP_is_show() == 0) {
                ArrayList<Product> t_products = new ArrayList<Product>();
                t_products.add(product);
                int j = i + 1;
                while (j < m_products.size()) {
                    if (m_products.get(j).getP_is_show() == 0 && product.getP_color().equals(m_products.get(j).getP_color()) && product.getP_weight() == m_products.get(j).getP_weight()) {
                        t_products.add(m_products.get(j));
                        m_products.get(j).setP_is_show(1);
                    }
                    ++j;
                }
                m_products_map.put(String.valueOf(product.getP_weight()) + "*" + product.getP_color(), t_products);
                product = null;
                t_products = null;
            }
            ++i;
        }
        System.out.println("\u4ea7\u54c1\u5206\u7ec4\u7ed3\u675f");
        return m_products_map;
    }

    public Map<String, List<Product>> scoreProduct(Map<String, List<Product>> m_products_map) {
        Iterator<String> it = m_products_map.keySet().iterator();
        while (it.hasNext()) {
        }
        return m_products_map;
    }
}
