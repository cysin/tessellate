/*
 * Decompiled with CFR 0.152.
 */
package com.gv.service;

import com.gv.model.Material;
import com.gv.model.Product;
import com.gv.tool.CommonTools;
import com.gv.tool.DecimalMath;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Vector;

public class ViewServiceN {
    public List<Material> createView(List<Product> m_products, List<Material> m_materials, double saw_bite) {
        ArrayList<Material> b_b_materials = new ArrayList<Material>();
        Product product = null;
        Map<String, List<Product>> m_products_map = this.processProduct(m_products);
        Map<String, List<Material>> m_materials_map = this.processMaterial(m_materials);
        for (String key : m_products_map.keySet()) {
            m_products = m_products_map.get(key);
            List<Product> mm_products = this.scoreAreaProduct(m_products);
            m_materials = CommonTools.cloneMatList(m_materials_map.get(key));
            if ((m_materials = this.scoreMaterial(m_materials)) == null) continue;
            Material material = null;
            int i = 0;
            if (i >= m_materials.size()) continue;
            if (0.0 >= m_materials.get(i).getM_count()) {
                System.out.println("\u677f\u6750\u4e0d\u591f\u4e86");
                continue;
            }
            int node_id = 0;
            material = CommonTools.cloneScheme(m_materials.get(i));
            if (1.0 == material.getM_count()) {
                System.out.println("\u539f\u6599:" + material.getM_name() + "\u7528\u5b8c\u4e86\uff01");
                m_materials.remove(i);
            } else {
                m_materials.get(i).setM_count(material.getM_count() - 1.0);
            }
            ArrayList<Material> d_materials = new ArrayList<Material>();
            d_materials.add(material);
            List<Material> m_ms = null;
            boolean f = true;
            while (f) {
                if (m_ms == null) {
                    m_ms = new ArrayList<Material>();
                    m_ms.add(material);
                } else {
                    mm_products = this.scoreProduct(mm_products, 0);
                }
                ArrayList<Material> t_materials = new ArrayList<Material>();
                for (Material m_material : m_ms) {
                    int j = 0;
                    while (j < mm_products.size()) {
                        product = mm_products.get(j);
                        if (product.getP_r_count() > 0) {
                            ArrayList<Product> m_ps = new ArrayList<Product>();
                            if (m_material.getR_width() == product.getP_width() && m_material.getR_height() == product.getP_height() || m_material.getR_width() == product.getP_width() && m_material.getR_height() >= product.getP_height() + saw_bite || m_material.getR_width() >= product.getP_width() + saw_bite && m_material.getR_height() == product.getP_height() || m_material.getR_width() >= product.getP_width() + saw_bite && m_material.getR_height() >= product.getP_height() + saw_bite) {
                                Product p = CommonTools.clonePro(product);
                                p.setM_left(m_material.getM_m_left());
                                p.setM_top(m_material.getM_m_top());
                                m_ps.add(p);
                                p = null;
                                m_material.setM_products(m_ps);
                                for (Product t_p : mm_products) {
                                    if (product.getP_is_dir() == 0) {
                                        if (product.getP_name().equals(t_p.getP_name()) && product.getP_width() == t_p.getP_width() && product.getP_height() == t_p.getP_height()) {
                                            t_p.setP_r_count(t_p.getP_r_count() - 1);
                                            continue;
                                        }
                                        if (!product.getP_name().equals(t_p.getP_name()) || product.getP_width() != t_p.getP_height() || product.getP_width() != t_p.getP_height()) continue;
                                        t_p.setP_r_count(t_p.getP_r_count() - 1);
                                        continue;
                                    }
                                    if (!product.getP_name().equals(t_p.getP_name()) || product.getP_width() != t_p.getP_width() || product.getP_height() != t_p.getP_height() || product.getP_is_dir() != t_p.getP_is_dir()) continue;
                                    t_p.setP_r_count(t_p.getP_r_count() - 1);
                                    System.out.println("\u751f\u4ea7\u4e86" + t_p.getP_name());
                                }
                                m_material.setM_products(m_ps);
                                Material t_material = new Material();
                                t_material.setR_height(DecimalMath.mul(DecimalMath.mul(m_material.getR_height(), product.getP_height()), saw_bite));
                                t_material.setR_width(m_material.getR_width());
                                t_material.setM_width(m_material.getM_width());
                                t_material.setM_height(m_material.getM_height());
                                t_material.setM_f_id(m_material.getM_node_id());
                                t_material.setM_node_id(++node_id);
                                t_material.setM_c_type(0);
                                t_material.setM_hs_type(1);
                                t_material.setM_m_left(0.0);
                                t_material.setM_m_top(product.getP_height() + saw_bite);
                                t_materials.add(t_material);
                                t_material = new Material();
                                t_material.setR_height(product.getP_height());
                                t_material.setR_width(DecimalMath.mul(DecimalMath.mul(m_material.getR_width(), product.getP_width()), saw_bite));
                                t_material.setM_width(m_material.getM_width());
                                t_material.setM_height(m_material.getM_height());
                                t_material.setM_f_id(m_material.getM_node_id());
                                t_material.setM_node_id(++node_id);
                                t_material.setM_c_type(0);
                                t_material.setM_hs_type(0);
                                t_material.setM_m_left(product.getP_width() + saw_bite);
                                t_material.setM_m_top(0.0);
                                t_materials.add(t_material);
                                j = mm_products.size();
                            }
                        }
                        ++j;
                    }
                }
                if (t_materials.size() == 0) {
                    f = false;
                    continue;
                }
                d_materials.addAll(t_materials);
                m_ms = CommonTools.cloneMatList(t_materials);
                t_materials = new ArrayList();
            }
            Material b_material = new Material();
            for (Material d_m : d_materials) {
                if (d_m.getM_products() == null) continue;
                if (b_material.getM_products() == null) {
                    b_material.setM_products(d_m.getM_products());
                    continue;
                }
                b_material.getM_products().addAll(d_m.getM_products());
            }
            b_b_materials.add(b_material);
        }
        return b_b_materials;
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

    public List<Material> scoreYMaterial(List<Material> materials, int score_type) {
        List<Material> l_materials = materials;
        Material t_material = null;
        switch (score_type) {
            case 0: {
                int i = 0;
                while (i < l_materials.size()) {
                    Material material = l_materials.get(i);
                    int j = i + 1;
                    while (j < l_materials.size()) {
                        if (material.getM_m_left() > l_materials.get(j).getM_m_left()) {
                            t_material = l_materials.get(j);
                            l_materials.set(i, t_material);
                            l_materials.set(j, material);
                            material = l_materials.get(i);
                        } else if (material.getM_m_left() == l_materials.get(j).getM_m_left() && material.getM_m_top() > l_materials.get(j).getM_m_top()) {
                            t_material = l_materials.get(j);
                            l_materials.set(i, t_material);
                            l_materials.set(j, material);
                            material = l_materials.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break;
            }
            case 1: {
                int i = 0;
                while (i < l_materials.size()) {
                    Material material = l_materials.get(i);
                    int j = i + 1;
                    while (j < l_materials.size()) {
                        if (material.getM_m_top() > l_materials.get(j).getM_m_top()) {
                            t_material = l_materials.get(j);
                            l_materials.set(i, t_material);
                            l_materials.set(j, material);
                            material = l_materials.get(i);
                        } else if (material.getM_m_top() == l_materials.get(j).getM_m_top() && material.getM_m_left() > l_materials.get(j).getM_m_left()) {
                            t_material = l_materials.get(j);
                            l_materials.set(i, t_material);
                            l_materials.set(j, material);
                            material = l_materials.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break;
            }
        }
        return l_materials;
    }

    public List<Material> scoreMaterial(List<Material> materials) {
        int j;
        Material material;
        List<Material> l_materials = CommonTools.cloneMatList(materials);
        Material t_material = null;
        int i = 0;
        while (i < l_materials.size()) {
            material = l_materials.get(i);
            if (material.getM_is_yl() == 0) {
                j = i + 1;
                while (j < l_materials.size()) {
                    if (1 == l_materials.get(j).getM_is_yl()) {
                        t_material = l_materials.get(j);
                        l_materials.set(i, t_material);
                        l_materials.set(j, material);
                        material = l_materials.get(i);
                    }
                    ++j;
                }
            }
            ++i;
        }
        i = 0;
        while (i < l_materials.size()) {
            material = l_materials.get(i);
            if (1 == material.getM_is_yl()) {
                j = i + 1;
                while (j < l_materials.size()) {
                    if (1 == l_materials.get(j).getM_is_yl()) {
                        if (material.getR_height() < l_materials.get(j).getR_height()) {
                            t_material = l_materials.get(j);
                            l_materials.set(i, t_material);
                            l_materials.set(j, material);
                            material = l_materials.get(i);
                        } else if (material.getR_height() == l_materials.get(j).getR_height() && material.getR_width() < l_materials.get(j).getR_width()) {
                            t_material = l_materials.get(j);
                            l_materials.set(i, t_material);
                            l_materials.set(j, material);
                            material = l_materials.get(i);
                        }
                    }
                    ++j;
                }
            }
            ++i;
        }
        return l_materials;
    }

    public List<Product> scoreProduct(List<Product> products, int score_type) {
        Product t_product = null;
        switch (score_type) {
            case 0: {
                int i = 0;
                while (i < products.size()) {
                    Product product = products.get(i);
                    int j = i + 1;
                    while (j < products.size()) {
                        if (product.getP_height() < products.get(j).getP_height()) {
                            t_product = products.get(j);
                            products.set(i, t_product);
                            products.set(j, product);
                            product = products.get(i);
                        } else if (product.getP_height() == products.get(j).getP_height() && product.getP_width() < products.get(j).getP_width()) {
                            t_product = products.get(j);
                            products.set(i, t_product);
                            products.set(j, product);
                            product = products.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break;
            }
            case 9: {
                int i = 0;
                while (i < products.size()) {
                    Product product = products.get(i);
                    int j = i + 1;
                    while (j < products.size()) {
                        if (product.getP_width() < products.get(j).getP_width()) {
                            t_product = products.get(j);
                            products.set(i, t_product);
                            products.set(j, product);
                            product = products.get(i);
                        } else if (product.getP_width() == products.get(j).getP_width() && product.getP_height() < products.get(j).getP_height()) {
                            t_product = products.get(j);
                            products.set(i, t_product);
                            products.set(j, product);
                            product = products.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break;
            }
            default: {
                int i = 0;
                while (i < products.size()) {
                    Product product = products.get(i);
                    int j = i + 1;
                    while (j < products.size()) {
                        if (product.getP_width() * 0.1 * (double)score_type + product.getP_height() * (1.0 - 0.1 * (double)score_type) < products.get(j).getP_width() * 0.1 * (double)score_type + products.get(j).getP_height() * (1.0 - 0.1 * (double)score_type)) {
                            t_product = products.get(j);
                            products.set(i, t_product);
                            products.set(j, product);
                            product = products.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break block0;
            }
        }
        return products;
    }

    /*
     * WARNING - void declaration
     */
    private List<Product> queryUsedProducts(Material m_material, Map<Integer, Vector<List<Material>>> materials_map_index, int vt_index, List<Material> m_materials, Vector<List<Material>> vc) {
        void var8_15;
        void var8_13;
        Vector<List<Material>> v_t;
        ArrayList<Product> usedProducts = new ArrayList<Product>();
        Vector<Integer> t_n_id = new Vector<Integer>();
        System.out.println("\u67e5\u627e\u5f00\u59cb");
        if (1 < vt_index) {
            void var8_9;
            t_n_id.add(m_material.getM_f_id());
            int n = vt_index - 1;
            while (var8_9 > 0) {
                void var10_17;
                v_t = materials_map_index.get((int)var8_9);
                for (List list : v_t) {
                    for (Object v_m : list) {
                        if (!t_n_id.contains(((Material)v_m).getM_node_id())) continue;
                        t_n_id.add(((Material)v_m).getM_f_id());
                    }
                }
                void var10_19 = var8_9;
                while (var10_17 < vt_index) {
                    Object v_m;
                    v_t = materials_map_index.get((int)var8_9);
                    v_m = v_t.iterator();
                    while (v_m.hasNext()) {
                        List v_ms = (List)v_m.next();
                        Iterator iterator = v_ms.iterator();
                        while (iterator.hasNext()) {
                            Material v_m2 = (Material)iterator.next();
                            if (!t_n_id.contains(v_m2.getM_f_id())) continue;
                            t_n_id.add(v_m2.getM_node_id());
                        }
                    }
                    ++var10_17;
                }
                --var8_9;
            }
        }
        for (Material material : m_materials) {
            t_n_id.add(material.getM_node_id());
        }
        for (List list : vc) {
            for (Material material : list) {
                if (!t_n_id.contains(material.getM_f_id())) continue;
                t_n_id.add(material.getM_node_id());
            }
        }
        int n = vt_index - 1;
        while (var8_13 > 0) {
            v_t = materials_map_index.get((int)var8_13);
            for (List list : v_t) {
                for (Object v_m : list) {
                    if (!t_n_id.contains(((Material)v_m).getM_node_id()) || ((Material)v_m).getM_products() == null) continue;
                    usedProducts.addAll(CommonTools.cloneProList(((Material)v_m).getM_products()));
                }
            }
            --var8_13;
        }
        System.out.println(usedProducts.size());
        boolean bl = false;
        while (var8_15 < usedProducts.size()) {
            Product p_i = (Product)usedProducts.get((int)var8_15);
            if (p_i.getP_is_score() == 0) {
                void var10_23;
                p_i.setP_p_count(1);
                void var10_22 = var8_15 + true;
                while (var10_23 < usedProducts.size()) {
                    Product p_j = (Product)usedProducts.get((int)var10_23);
                    if (p_j.getP_is_score() == 0) {
                        if (p_i.getP_is_dir() == 0) {
                            if (p_i.getP_name().equals(p_j.getP_name()) && p_i.getP_width() == p_j.getP_width() && p_i.getP_height() == p_j.getP_height() && p_i.getP_is_copy() == p_j.getP_is_copy()) {
                                p_i.setP_p_count(p_i.getP_p_count() + 1);
                                p_j.setP_is_score(1);
                            } else if (p_i.getP_name().equals(p_j.getP_name()) && p_i.getP_width() == p_j.getP_height() && p_i.getP_height() == p_j.getP_width() && 1 == p_i.getP_is_copy() + p_j.getP_is_copy()) {
                                p_i.setP_p_count(p_i.getP_p_count() + 1);
                                p_j.setP_is_score(1);
                            }
                        } else if (p_i.getP_name().equals(p_j.getP_name()) && p_i.getP_width() == p_j.getP_width() && p_i.getP_height() == p_j.getP_height() && p_i.getP_is_copy() == p_j.getP_is_copy()) {
                            p_i.setP_p_count(p_i.getP_p_count() + 1);
                            p_j.setP_is_score(1);
                        }
                    }
                    ++var10_23;
                }
            }
            ++var8_15;
        }
        System.out.println("\u67e5\u627e\u7ed3\u675f");
        return usedProducts;
    }

    private boolean checkIsProductd(List<Product> u_products, Product p_product) {
        boolean result = true;
        if (p_product.getP_is_dir() == 0) {
            for (Product u_p : u_products) {
                if (u_p.getP_is_score() != 0) continue;
                if (u_p.getP_name().equals(p_product.getP_name()) && u_p.getP_width() == p_product.getP_width() && u_p.getP_height() == p_product.getP_height() && u_p.getP_is_copy() == p_product.getP_is_copy()) {
                    if (u_p.getP_p_count() < p_product.getP_r_count()) {
                        result = true;
                        continue;
                    }
                    result = false;
                    continue;
                }
                if (!u_p.getP_name().equals(p_product.getP_name()) || u_p.getP_width() != p_product.getP_height() || u_p.getP_height() != p_product.getP_width() || 1 != u_p.getP_is_copy() + p_product.getP_is_copy()) continue;
                result = u_p.getP_p_count() < p_product.getP_r_count();
            }
        } else {
            for (Product u_p : u_products) {
                if (!u_p.getP_name().equals(p_product.getP_name()) || u_p.getP_width() != p_product.getP_width() || u_p.getP_height() != p_product.getP_height() || u_p.getP_is_copy() != p_product.getP_is_copy()) continue;
                result = u_p.getP_p_count() < p_product.getP_r_count();
            }
        }
        return result;
    }

    public List<Product> scoreAreaProduct(List<Product> products) {
        List<Product> l_products = CommonTools.cloneProList(products);
        Product t_product = null;
        int i = 0;
        while (i < l_products.size()) {
            Product product = l_products.get(i);
            int j = i + 1;
            while (j < l_products.size()) {
                if (product.getP_height() * product.getP_width() < l_products.get(j).getP_height() * l_products.get(j).getP_width()) {
                    t_product = l_products.get(j);
                    l_products.set(i, t_product);
                    l_products.set(j, product);
                    product = l_products.get(i);
                }
                ++j;
            }
            ++i;
        }
        return l_products;
    }
}
