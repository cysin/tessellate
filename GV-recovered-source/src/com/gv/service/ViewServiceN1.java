/*
 * Decompiled with CFR 0.152.
 */
package com.gv.service;

import com.gv.model.Material;
import com.gv.model.Product;
import com.gv.tool.CommonTools;
import com.gv.tool.DecimalMath;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.Vector;

public class ViewServiceN1 {
    /*
     * Could not resolve type clashes
     */
    public List<Material> createView(List<Product> m_products, List<Material> m_materials, double saw_bite) {
        ArrayList<Material> materials = null;
        ArrayList<Material> b_b_materials = new ArrayList<Material>();
        ArrayList<Material> b_materials = null;
        Product product = null;
        Material m_material = null;
        Map<String, List<Product>> m_products_map = this.processProduct(m_products);
        Map<String, List<Material>> m_materials_map = this.processMaterial(m_materials);
        Iterator<String> it = m_products_map.keySet().iterator();
        int p_count = 0;
        int m_m_no = 0;
        while (it.hasNext()) {
            int j;
            String key = it.next();
            m_products = m_products_map.get(key);
            Vector b_materials_vc = new Vector();
            int flag = 0;
            while (flag < 10) {
                materials = new ArrayList<Material>();
                List<Product> mm_products = this.scoreAreaProduct(m_products);
                if (mm_products.size() > 0) {
                    m_m_no = 0;
                    p_count = -1;
                    m_materials = CommonTools.cloneMatList(m_materials_map.get(key));
                    if ((m_materials = this.scoreMaterial(m_materials)) == null) {
                        System.out.println("\u6ca1\u6709\u9002\u5408\u7684\u677f\u6750");
                    } else {
                        Material material = new Material();
                        Material b_material = null;
                        int i = 0;
                        while (i < m_materials.size()) {
                            m_material = m_materials.get(i);
                            if (0.0 >= m_material.getM_count()) {
                                System.out.println("\u677f\u6750\u4e0d\u591f\u4e86");
                                break;
                            }
                            ArrayList<Product> m_ps = new ArrayList<Product>();
                            j = 0;
                            while (j < mm_products.size()) {
                                Product p = mm_products.get(j);
                                if (!(m_material.getR_height() < p.getP_height()) && !(m_material.getR_width() < p.getP_width())) {
                                    int node_id = 0;
                                    p_count = (int)((m_material.getR_height() + saw_bite) / (p.getP_height() + saw_bite));
                                    if (p_count == 0) {
                                        System.out.println("\u4ea7\u54c1\u8fc7\u5927");
                                    } else {
                                        p_count = (int)((m_material.getR_width() + saw_bite) / (p.getP_width() + saw_bite));
                                        if (p_count == 0) {
                                            System.out.println("\u4ea7\u54c1\u8fc7\u5927");
                                        } else {
                                            m_m_no = i;
                                            product = mm_products.get(j);
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
                                                System.out.println("\u539f\u6599:" + material.getM_name() + "\u7528\u5b8c\u4e86\uff01");
                                                m_materials.remove(m_m_no);
                                            } else {
                                                m_materials.get(m_m_no).setM_count(material.getM_count() - 1.0);
                                            }
                                            p = new Product();
                                            p.setM_left(0.0);
                                            p.setM_top(0.0);
                                            p.setP_no(product.getP_no());
                                            p.setP_name(product.getP_name());
                                            p.setP_height(product.getP_height());
                                            p.setP_width(product.getP_width());
                                            p.setP_is_copy(product.getP_is_copy());
                                            p.setP_is_dir(product.getP_is_dir());
                                            p.setP_is_show(0);
                                            m_ps.add(p);
                                            p = null;
                                            material.setM_products(m_ps);
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
                                            int index = 1;
                                            TreeMap<String, List<Material>> t_materials_map = new TreeMap<String, List<Material>>();
                                            TreeMap materials_map_index = new TreeMap();
                                            TreeMap<Integer, Material> material_map = new TreeMap<Integer, Material>();
                                            material_map.put(node_id, material);
                                            Vector vt = new Vector();
                                            ArrayList<Material> t_materials = null;
                                            Material t_material = null;
                                            Material p_material = null;
                                            t_materials = new ArrayList<Material>();
                                            t_material = CommonTools.cloneScheme(material);
                                            t_material.setR_height(DecimalMath.mul(DecimalMath.mul(material.getR_height(), product.getP_height()), saw_bite));
                                            t_material.setR_width(material.getR_width());
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_f_f_id(material.getM_f_id());
                                            t_material.setM_node_id(++node_id);
                                            t_material.setM_c_type(0);
                                            t_material.setM_hs_type(1);
                                            t_material.setM_m_left(0.0);
                                            t_material.setM_m_top(product.getP_height() + saw_bite);
                                            t_materials.add(t_material);
                                            material_map.put(node_id, t_material);
                                            t_material = CommonTools.cloneScheme(material);
                                            t_material.setR_height(product.getP_height());
                                            t_material.setR_width(DecimalMath.mul(DecimalMath.mul(material.getR_width(), product.getP_width()), saw_bite));
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_f_f_id(material.getM_f_id());
                                            t_material.setM_node_id(++node_id);
                                            t_material.setM_c_type(0);
                                            t_material.setM_hs_type(0);
                                            t_material.setM_m_left(product.getP_width() + saw_bite);
                                            t_material.setM_m_top(0.0);
                                            t_materials.add(t_material);
                                            material_map.put(node_id, t_material);
                                            p_material = CommonTools.cloneScheme(material);
                                            p_material.setM_is_p_info(1);
                                            p_material.setM_c_type(0);
                                            p_material.setM_node_id(++node_id);
                                            t_materials.add(p_material);
                                            vt.add(t_materials);
                                            t_materials = new ArrayList();
                                            t_material = CommonTools.cloneScheme(material);
                                            t_material.setR_height(DecimalMath.mul(DecimalMath.mul(material.getR_height(), product.getP_height()), saw_bite));
                                            t_material.setR_width(product.getP_width());
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_f_f_id(material.getM_f_id());
                                            t_material.setM_node_id(++node_id);
                                            t_material.setM_c_type(1);
                                            t_material.setM_hs_type(1);
                                            t_material.setM_m_left(0.0);
                                            t_material.setM_m_top(product.getP_height() + saw_bite);
                                            t_materials.add(t_material);
                                            material_map.put(node_id, t_material);
                                            t_material = CommonTools.cloneScheme(material);
                                            t_material.setR_height(material.getR_height());
                                            t_material.setR_width(DecimalMath.mul(DecimalMath.mul(material.getR_width(), product.getP_width()), saw_bite));
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_f_f_id(material.getM_f_id());
                                            t_material.setM_node_id(++node_id);
                                            t_material.setM_c_type(1);
                                            t_material.setM_hs_type(0);
                                            t_material.setM_m_left(product.getP_width() + saw_bite);
                                            t_material.setM_m_top(0.0);
                                            t_materials.add(t_material);
                                            material_map.put(node_id, t_material);
                                            p_material = CommonTools.cloneScheme(material);
                                            p_material.setM_is_p_info(1);
                                            p_material.setM_c_type(1);
                                            p_material.setM_node_id(++node_id);
                                            t_materials.add(p_material);
                                            material_map.put(node_id, p_material);
                                            vt.add(t_materials);
                                            material.setM_material_map(t_materials_map);
                                            materials_map_index.put(index, vt);
                                            Iterator it_t = materials_map_index.keySet().iterator();
                                            mm_products = this.scoreProduct(mm_products, flag);
                                            while (it_t.hasNext()) {
                                                vt = (Vector)materials_map_index.get(index);
                                                Vector<ArrayList<Material>> vt_t = new Vector<ArrayList<Material>>();
                                                if (vt.size() == 0) break;
                                                for (List materials_index : vt) {
                                                    block7: for (Material t_m : materials_index) {
                                                        if (t_m.getM_is_p_info() != 0) continue;
                                                        for (Iterator t_p : mm_products) {
                                                            List<Product> u_products;
                                                            boolean r;
                                                            if (((Product)((Object)t_p)).getP_r_count() <= 0 || !(t_m.getR_width() == product.getP_width() && t_m.getR_height() == product.getP_height() || t_m.getR_width() == product.getP_width() && t_m.getR_height() >= product.getP_height() + saw_bite || t_m.getR_width() >= product.getP_width() + saw_bite && t_m.getR_height() == product.getP_height()) && (!(t_m.getR_width() >= product.getP_width() + saw_bite) || !(t_m.getR_height() >= product.getP_height() + saw_bite)) || !(r = this.checkIsProductd(u_products = this.queryUsedProducts(t_m, materials_index), (Product)((Object)t_p)))) continue;
                                                            m_ps = new ArrayList();
                                                            p = CommonTools.clonePro((Product)((Object)t_p));
                                                            p.setM_left(t_m.getM_m_left());
                                                            p.setM_top(t_m.getM_m_top());
                                                            m_ps.add(p);
                                                            p = null;
                                                            t_m.setM_products(m_ps);
                                                            t_materials = new ArrayList();
                                                            t_material = CommonTools.cloneScheme(t_m);
                                                            t_material.setR_height(t_m.getR_height() - ((Product)((Object)t_p)).getP_height() - saw_bite);
                                                            t_material.setR_width(t_m.getR_width());
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_f_f_id(t_m.getM_f_id());
                                                            t_material.setM_node_id(++node_id);
                                                            t_material.setM_c_type(0);
                                                            t_material.setM_hs_type(1);
                                                            t_material.setM_f_c_type(t_m.getM_c_type());
                                                            t_material.setM_m_left(t_m.getM_m_left());
                                                            t_material.setM_m_top(t_m.getM_m_top() + ((Product)((Object)t_p)).getP_height() + saw_bite);
                                                            t_materials.add(t_material);
                                                            material_map.put(node_id, t_material);
                                                            t_material = CommonTools.cloneScheme(t_m);
                                                            t_material.setR_height(((Product)((Object)t_p)).getP_height());
                                                            t_material.setR_width(t_m.getR_width() - ((Product)((Object)t_p)).getP_width() - saw_bite);
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_f_f_id(t_m.getM_f_id());
                                                            t_material.setM_node_id(++node_id);
                                                            t_material.setM_c_type(0);
                                                            t_material.setM_hs_type(0);
                                                            t_material.setM_f_c_type(t_m.getM_c_type());
                                                            t_material.setM_m_left(t_m.getM_m_left() + ((Product)((Object)t_p)).getP_width() + saw_bite);
                                                            t_material.setM_m_top(t_m.getM_m_top());
                                                            t_materials.add(t_material);
                                                            material_map.put(node_id, t_material);
                                                            p_material = CommonTools.cloneScheme(t_m);
                                                            p_material.setM_is_p_info(1);
                                                            p_material.setM_node_id(++node_id);
                                                            p_material.setM_f_id(t_m.getM_node_id());
                                                            p_material.setM_f_f_id(t_m.getM_f_id());
                                                            p_material.setM_f_c_type(t_m.getM_c_type());
                                                            p_material.setM_c_type(0);
                                                            t_materials.add(p_material);
                                                            material_map.put(node_id, p_material);
                                                            vt_t.add(t_materials);
                                                            t_materials = new ArrayList();
                                                            t_material = CommonTools.cloneScheme(t_m);
                                                            t_material.setR_height(t_m.getR_height() - ((Product)((Object)t_p)).getP_height() - saw_bite);
                                                            t_material.setR_width(((Product)((Object)t_p)).getP_width());
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_f_f_id(t_m.getM_f_id());
                                                            t_material.setM_node_id(++node_id);
                                                            t_material.setM_c_type(1);
                                                            t_material.setM_f_c_type(t_m.getM_c_type());
                                                            t_material.setM_hs_type(1);
                                                            t_material.setM_m_left(t_m.getM_m_left());
                                                            t_material.setM_m_top(t_m.getM_m_top() + ((Product)((Object)t_p)).getP_height() + saw_bite);
                                                            t_materials.add(t_material);
                                                            material_map.put(node_id, t_material);
                                                            t_material = CommonTools.cloneScheme(t_m);
                                                            t_material.setR_height(t_m.getR_height());
                                                            t_material.setR_width(t_m.getR_width() - ((Product)((Object)t_p)).getP_width() - saw_bite);
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_f_f_id(t_m.getM_f_id());
                                                            t_material.setM_node_id(++node_id);
                                                            t_material.setM_c_type(1);
                                                            t_material.setM_f_c_type(t_m.getM_c_type());
                                                            t_material.setM_hs_type(0);
                                                            t_material.setM_m_left(t_m.getM_m_left() + ((Product)((Object)t_p)).getP_width() + saw_bite);
                                                            t_material.setM_m_top(t_m.getM_m_top());
                                                            t_materials.add(t_material);
                                                            material_map.put(node_id, t_material);
                                                            p_material = CommonTools.cloneScheme(t_m);
                                                            p_material.setM_is_p_info(1);
                                                            p_material.setM_node_id(++node_id);
                                                            p_material.setM_f_id(t_m.getM_node_id());
                                                            p_material.setM_f_f_id(t_m.getM_f_id());
                                                            p_material.setM_f_c_type(t_m.getM_c_type());
                                                            p_material.setM_c_type(1);
                                                            t_materials.add(p_material);
                                                            material_map.put(node_id, p_material);
                                                            vt_t.add(t_materials);
                                                            continue block7;
                                                        }
                                                    }
                                                }
                                                Vector<List<Material>> vt_tt = new Vector<List<Material>>();
                                                boolean ff = false;
                                                int v_i = 0;
                                                while (v_i < vt_t.size()) {
                                                    Iterator t_p;
                                                    t_p = ((List)vt_t.get(v_i)).iterator();
                                                    if (t_p.hasNext()) {
                                                        Material m = (Material)t_p.next();
                                                        int v_j = v_i + 1;
                                                        while (v_j < vt_t.size()) {
                                                            Iterator r = ((List)vt_t.get(v_j)).iterator();
                                                            if (r.hasNext()) {
                                                                Material m_m = (Material)r.next();
                                                                if (m.getM_f_id() != m_m.getM_f_id() && m.getM_f_f_id() == m_m.getM_f_f_id() && m.getM_f_c_type() == m_m.getM_f_c_type()) {
                                                                    List<Material> n_ms = CommonTools.cloneMatList((List)vt_t.get(v_i));
                                                                    n_ms.addAll(CommonTools.cloneMatList((List)vt_t.get(v_j)));
                                                                    ff = true;
                                                                    vt_tt.add(n_ms);
                                                                }
                                                            }
                                                            ++v_j;
                                                        }
                                                        if (!ff) {
                                                            vt_tt.add(CommonTools.cloneMatList((List)vt_t.get(v_i)));
                                                        }
                                                    }
                                                    ++v_i;
                                                }
                                                v_i = 0;
                                                while (v_i < vt_tt.size()) {
                                                    boolean tag = false;
                                                    int v_j = 0;
                                                    while (v_j < ((List)vt_tt.get(v_i)).size()) {
                                                        if (1 == ((Material)((List)vt_tt.get(v_i)).get(v_j)).getM_is_p_info() && !tag) {
                                                            int v_jj = v_j + 1;
                                                            while (v_jj < ((List)vt_tt.get(v_i)).size()) {
                                                                if (1 == ((Material)((List)vt_tt.get(v_i)).get(v_jj)).getM_is_p_info()) {
                                                                    ((Material)((List)vt_tt.get(v_i)).get(v_j)).getM_products().addAll(((Material)((List)vt_tt.get(v_i)).get(v_jj)).getM_products());
                                                                    ((List)vt_tt.get(v_i)).remove(v_jj);
                                                                    --v_jj;
                                                                    --v_j;
                                                                }
                                                                ++v_jj;
                                                            }
                                                            tag = true;
                                                        }
                                                        ++v_j;
                                                    }
                                                    ++v_i;
                                                }
                                                for (List ms_tt : vt_tt) {
                                                    for (Material m_tt : ms_tt) {
                                                        if (1 != m_tt.getM_is_p_info()) continue;
                                                        for (List ms_t : vt) {
                                                            for (Material m_t : ms_t) {
                                                                if (1 != m_t.getM_is_p_info() || m_tt.getM_f_f_id() != m_t.getM_f_id() || m_tt.getM_f_c_type() != m_t.getM_c_type()) continue;
                                                                m_tt.getM_products().addAll(m_t.getM_products());
                                                            }
                                                        }
                                                    }
                                                }
                                                for (List ms_tt : vt_tt) {
                                                    for (Material m_tt : ms_tt) {
                                                        if (1 != m_tt.getM_is_p_info()) continue;
                                                        int p_i = 0;
                                                        while (p_i < m_tt.getM_products().size()) {
                                                            Product pi = m_tt.getM_products().get(p_i);
                                                            int p_j = p_i + 1;
                                                            while (p_j < m_tt.getM_products().size()) {
                                                                Product pj = m_tt.getM_products().get(p_j);
                                                                if (pi.getM_left() == pj.getM_left() && pi.getM_top() == pj.getM_top()) {
                                                                    m_tt.getM_products().remove(p_j);
                                                                    --p_j;
                                                                }
                                                                ++p_j;
                                                            }
                                                            ++p_i;
                                                        }
                                                    }
                                                }
                                                materials_map_index.put(++index, vt_tt);
                                                it_t = materials_map_index.keySet().iterator();
                                            }
                                            b_materials = new ArrayList<Material>();
                                            Iterator it_i = materials_map_index.keySet().iterator();
                                            while (it_i.hasNext()) {
                                                Vector b_vc = (Vector)materials_map_index.get(it_i.next());
                                                for (List b_ms : b_vc) {
                                                    for (Material b_m : b_ms) {
                                                        if (1 != b_m.getM_is_p_info()) continue;
                                                        b_material = CommonTools.cloneScheme(b_m);
                                                        b_materials.add(b_material);
                                                    }
                                                }
                                            }
                                            System.out.println(b_materials.size());
                                            for (Material b_m : b_materials) {
                                                for (Product b_p : b_m.getM_products()) {
                                                    b_m.setM_area_used(DecimalMath.add(b_m.getM_area_used(), DecimalMath.sub(b_p.getP_height(), b_p.getP_width())));
                                                }
                                            }
                                            for (Material b_m : b_materials) {
                                                b_m.setM_area_used(b_m.getM_area_used() / DecimalMath.sub(b_m.getM_height(), b_m.getM_width()));
                                            }
                                            b_material = (Material)b_materials.get(0);
                                            int b_i = 1;
                                            while (b_i < b_materials.size()) {
                                                if (((Material)b_materials.get(b_i)).getM_area_used() > b_material.getM_area_used()) {
                                                    b_material = (Material)b_materials.get(b_i);
                                                }
                                                ++b_i;
                                            }
                                            for (Product p_p : b_material.getM_products()) {
                                                for (Product t_p : mm_products) {
                                                    if (p_p.getP_is_dir() == 0) {
                                                        if (p_p.getP_name().equals(t_p.getP_name()) && p_p.getP_width() == t_p.getP_width() && p_p.getP_height() == t_p.getP_height()) {
                                                            t_p.setP_count(t_p.getP_count() - 1.0);
                                                            continue;
                                                        }
                                                        if (!p_p.getP_name().equals(t_p.getP_name()) || p_p.getP_width() != t_p.getP_height() || p_p.getP_width() != t_p.getP_height()) continue;
                                                        t_p.setP_count(t_p.getP_count() - 1.0);
                                                        continue;
                                                    }
                                                    if (!p_p.getP_name().equals(t_p.getP_name()) || p_p.getP_width() != t_p.getP_width() || p_p.getP_height() != t_p.getP_height() || p_p.getP_is_dir() != t_p.getP_is_dir()) continue;
                                                    t_p.setP_count(t_p.getP_count() - 1.0);
                                                    System.out.println("\u751f\u4ea7\u4e86" + t_p.getP_name());
                                                }
                                            }
                                            for (Product t_p : mm_products) {
                                                t_p.setP_r_count((int)t_p.getP_count());
                                            }
                                            int ll = 0;
                                            while (ll < mm_products.size()) {
                                                if (0.0 >= mm_products.get(ll).getP_count()) {
                                                    System.out.println("\u6709\u4ea7\u54c1\u751f\u4ea7\u5b8c\u4e86");
                                                    mm_products.remove(ll);
                                                    --ll;
                                                }
                                                ++ll;
                                            }
                                            materials.add(b_material);
                                            if (mm_products.size() <= 0) {
                                                System.out.println("\u6240\u6709\u4ea7\u54c1\u751f\u4ea7\u5b8c\u4e86\uff01");
                                                b_materials_vc.add(materials);
                                                break;
                                            }
                                            --i;
                                            j = mm_products.size();
                                        }
                                    }
                                }
                                ++j;
                            }
                            ++i;
                        }
                        System.out.println("---------------");
                    }
                }
                ++flag;
            }
            b_materials = (ArrayList<Material>)b_materials_vc.get(0);
            int mmm = 1;
            while (mmm < b_materials_vc.size()) {
                if (((List)b_materials_vc.get(mmm)).size() < b_materials.size()) {
                    b_materials = (List)b_materials_vc.get(mmm);
                    System.out.println("\u6700\u4f18\u5f00\u677f\u7b97\u6cd5\u662f" + mmm);
                }
                ++mmm;
            }
            for (Material u_m : b_materials) {
                int i = 0;
                while (i < b_materials.size()) {
                    if (u_m.getM_is_show() == 0 && ((Material)b_materials.get(i)).getM_is_show() == 0 && u_m != b_materials.get(i) && u_m.getM_name().equals(((Material)b_materials.get(i)).getM_name()) && u_m.getR_height() == ((Material)b_materials.get(i)).getR_height() && ((Material)b_materials.get(i)).getR_width() == u_m.getR_width() && ((Material)b_materials.get(i)).getM_color().equals(u_m.getM_color()) && ((Material)b_materials.get(i)).getM_weight() == u_m.getM_weight() && ((Material)b_materials.get(i)).getM_products().size() == u_m.getM_products().size()) {
                        List<Product> u_m_products = u_m.getM_products();
                        List<Product> m_t_products = ((Material)b_materials.get(i)).getM_products();
                        int flag2 = 0;
                        j = 0;
                        while (j < u_m_products.size()) {
                            if (!u_m_products.get(j).getP_name().equals(m_t_products.get(j).getP_name()) || u_m_products.get(j).getM_left() != m_t_products.get(j).getM_left() || u_m_products.get(j).getM_top() != m_t_products.get(j).getM_top() || u_m_products.get(j).getP_width() != m_t_products.get(j).getP_width() || u_m_products.get(j).getP_height() != m_t_products.get(j).getP_height()) break;
                            ++flag2;
                            ++j;
                        }
                        if (flag2 == u_m_products.size()) {
                            u_m.setM_u_count(u_m.getM_u_count() + 1);
                            ((Material)b_materials.get(i)).setM_is_show(1);
                        }
                    }
                    ++i;
                }
            }
            for (Material mm : b_materials) {
                if (mm.getM_is_show() != 0) continue;
                ArrayList<Material> m_y_materials = new ArrayList<Material>();
                for (Product ppp : mm.getM_products()) {
                    Material y_m;
                    double l_point = ppp.getM_left() + ppp.getP_width() + saw_bite;
                    double t_point = ppp.getM_top() + ppp.getP_height() + saw_bite;
                    boolean l = false;
                    boolean t = false;
                    boolean d = false;
                    for (Product pppp : mm.getM_products()) {
                        if (t_point == pppp.getM_top() && l_point == pppp.getM_left()) {
                            d = true;
                            continue;
                        }
                        if (l_point == pppp.getM_left() && ppp.getM_top() == pppp.getM_top()) {
                            l = true;
                            continue;
                        }
                        if (t_point != pppp.getM_top() || ppp.getM_left() != pppp.getM_left()) continue;
                        t = true;
                    }
                    if (!l && 0.0 < mm.getR_width() - l_point) {
                        y_m = new Material();
                        y_m.setM_width(mm.getM_width());
                        y_m.setM_height(mm.getM_height());
                        y_m.setR_width(mm.getR_width() - l_point);
                        y_m.setR_height(ppp.getP_height());
                        y_m.setM_m_left(l_point);
                        y_m.setM_m_top(ppp.getM_top());
                        y_m.setM_y_is_ud(0);
                        m_y_materials.add(y_m);
                    }
                    if (!t && 0.0 < mm.getR_height() - t_point) {
                        y_m = new Material();
                        y_m.setM_width(mm.getM_width());
                        y_m.setM_height(mm.getM_height());
                        y_m.setR_width(ppp.getP_width());
                        y_m.setR_height(mm.getR_height() - t_point);
                        y_m.setM_m_left(ppp.getM_left());
                        y_m.setM_m_top(t_point);
                        y_m.setM_y_is_ud(1);
                        m_y_materials.add(y_m);
                    }
                    if (d || t || l || !(0.0 < mm.getR_height() - t_point) || !(0.0 < mm.getR_width() - l_point)) continue;
                    y_m = new Material();
                    y_m.setM_width(mm.getM_width());
                    y_m.setM_height(mm.getM_height());
                    y_m.setR_width(mm.getR_width() - l_point);
                    y_m.setR_height(mm.getR_height() - t_point);
                    y_m.setM_m_left(l_point);
                    y_m.setM_m_top(t_point);
                    y_m.setM_is_yj(1);
                    y_m.setM_y_is_ud(2);
                    m_y_materials.add(y_m);
                }
                for (Material y_material : m_y_materials) {
                    if (y_material.getM_is_show() != 0) continue;
                    for (Material y_t_material : m_y_materials) {
                        if (y_t_material.getM_is_show() != 0 || y_material == y_t_material || y_material.getM_m_left() != y_t_material.getM_m_left() || y_t_material.getM_m_top() != y_material.getM_m_top() + y_material.getR_height() + saw_bite || y_material.getR_width() != y_t_material.getR_width()) continue;
                        y_t_material.setM_is_show(1);
                        y_material.setR_height(y_material.getR_height() + y_t_material.getR_height() + saw_bite);
                    }
                }
                for (Material y_material : m_y_materials) {
                    if (y_material.getM_is_show() != 0) continue;
                    for (Material y_t_material : m_y_materials) {
                        if (y_t_material.getM_is_show() != 0 || y_material == y_t_material || y_t_material.getM_m_left() != y_material.getM_m_left() + y_material.getR_width() + saw_bite || y_material.getM_m_top() != y_t_material.getM_m_top() || y_material.getR_height() != y_t_material.getR_height()) continue;
                        y_t_material.setM_is_show(1);
                        y_material.setR_width(y_material.getR_width() + y_t_material.getR_width() + saw_bite);
                    }
                }
                for (Material y_material : m_y_materials) {
                    if (y_material.getM_is_show() != 0) continue;
                    for (Product y_t_p : mm.getM_products()) {
                        if (!(y_t_p.getM_left() >= y_material.getM_m_left()) || !(y_t_p.getM_left() <= y_material.getM_m_left() + y_material.getR_width()) || !(y_t_p.getM_top() >= y_material.getM_m_top()) || !(y_t_p.getM_top() <= y_material.getM_m_top() + y_material.getR_height())) continue;
                        y_material.setR_height(y_material.getR_height() - y_t_p.getP_height() - saw_bite);
                    }
                }
                for (Material y_material : m_y_materials) {
                    if (y_material.getM_is_show() != 0) continue;
                    for (Product y_t_p : mm.getM_products()) {
                        if (y_material.getM_m_left() != y_t_p.getM_left() || !(y_material.getM_m_top() >= y_t_p.getM_top()) || !(y_material.getM_m_top() <= y_t_p.getM_top() + y_t_p.getP_height()) || !(y_material.getR_width() >= y_t_p.getP_width())) continue;
                        System.out.println("\u6709\u90e8\u5206\u91cd\u5408\u7684\u4f59\u6599");
                        y_material.setR_width(y_material.getR_width() - y_t_p.getP_width() - saw_bite);
                        y_material.setM_m_left(y_material.getM_m_left() + y_t_p.getP_width() + saw_bite);
                    }
                }
                for (Material y_material : m_y_materials) {
                    if (y_material.getM_is_show() != 0) continue;
                    for (Product y_t_p : mm.getM_products()) {
                        double l_p_x1 = y_material.getM_m_left();
                        double l_p_y1 = y_material.getM_m_top() + y_material.getR_height();
                        double r_p_x1 = y_material.getM_m_left() + y_material.getR_width();
                        double r_p_y1 = y_material.getM_m_top();
                        double l_p_x2 = y_t_p.getM_left();
                        double l_p_y2 = y_t_p.getM_top() + y_t_p.getP_height();
                        double r_p_x2 = y_t_p.getM_left() + y_t_p.getP_width();
                        double r_p_y2 = y_t_p.getM_top();
                        if (!(r_p_x2 >= l_p_x1) || !(r_p_y2 >= l_p_y1) || !(l_p_x2 <= r_p_x1) || !(l_p_y2 <= r_p_y1)) continue;
                        System.out.println("\u91cd\u5408");
                        double h = (r_p_y2 <= r_p_y1 ? r_p_y2 : r_p_y1) - (l_p_y1 >= l_p_y2 ? l_p_y1 : l_p_y2);
                        y_material.setR_height(y_material.getR_height() - h);
                    }
                }
                for (Material y_material : m_y_materials) {
                    if (y_material.getM_is_show() != 0) continue;
                    for (Material y_t_material : m_y_materials) {
                        if (y_material == y_t_material || y_t_material.getM_is_show() != 0 || !(y_material.getM_m_left() >= y_t_material.getM_m_left()) || !(y_material.getM_m_left() <= y_t_material.getM_m_left() + y_t_material.getR_width()) || !(y_material.getM_m_top() >= y_t_material.getM_m_top()) || !(y_material.getM_m_top() <= y_t_material.getM_m_top() + y_t_material.getR_height())) continue;
                        if (!(y_material.getM_m_left() + y_material.getR_width() >= y_t_material.getM_m_left() && y_material.getM_m_left() + y_material.getR_width() <= y_t_material.getM_m_left() + y_t_material.getR_width() && y_material.getM_m_top() + y_material.getR_height() >= y_t_material.getM_m_top() && y_material.getM_m_top() + y_material.getR_height() <= y_t_material.getM_m_top() + y_t_material.getR_height())) {
                            System.out.println("\u6709\u91cd\u5408\u7684\u4f59\u6599");
                            y_t_material.setR_height(y_t_material.getR_height() - y_material.getR_height() - saw_bite);
                            continue;
                        }
                        y_material.setM_is_show(1);
                    }
                }
                mm.setM_y_materials(m_y_materials);
            }
            for (Material m_i_material : b_materials) {
                ArrayList<Product> i_products = new ArrayList<Product>();
                int i_i = 0;
                while (i_i < m_i_material.getM_products().size()) {
                    Product i_product = m_i_material.getM_products().get(i_i);
                    if (i_product.getP_is_score() == 0) {
                        i_product.setP_count(1.0);
                        i_product.setP_is_score(1);
                        int j_i = i_i + 1;
                        while (j_i < m_i_material.getM_products().size()) {
                            if (m_i_material.getM_products().get(j_i).getP_is_score() == 0) {
                                if (i_product.getP_is_dir() == 0) {
                                    if (i_product.getP_name().equals(m_i_material.getM_products().get(j_i).getP_name()) && i_product.getP_height() == m_i_material.getM_products().get(j_i).getP_height() && i_product.getP_width() == m_i_material.getM_products().get(j_i).getP_width() && i_product.getP_is_copy() == m_i_material.getM_products().get(j_i).getP_is_copy()) {
                                        i_product.setP_count(i_product.getP_count() + 1.0);
                                        m_i_material.getM_products().get(j_i).setP_is_score(1);
                                    } else if (i_product.getP_name().equals(m_i_material.getM_products().get(j_i).getP_name()) && i_product.getP_width() == m_i_material.getM_products().get(j_i).getP_height() && i_product.getP_height() == m_i_material.getM_products().get(j_i).getP_width() && 1 == i_product.getP_is_copy() + m_i_material.getM_products().get(j_i).getP_is_copy()) {
                                        i_product.setP_count(i_product.getP_count() + 1.0);
                                        m_i_material.getM_products().get(j_i).setP_is_score(1);
                                    }
                                } else if (i_product.getP_name().equals(m_i_material.getM_products().get(j_i).getP_name()) && i_product.getP_height() == m_i_material.getM_products().get(j_i).getP_height() && i_product.getP_width() == m_i_material.getM_products().get(j_i).getP_width()) {
                                    i_product.setP_count(i_product.getP_count() + 1.0);
                                    m_i_material.getM_products().get(j_i).setP_is_score(1);
                                }
                            }
                            ++j_i;
                        }
                        i_products.add(i_product);
                    }
                    ++i_i;
                }
                m_i_material.setM_i_products(i_products);
            }
            b_b_materials.addAll((Collection<Material>)b_materials);
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

    private List<Product> queryUsedProducts(Material t_m, List<Material> materials_index) {
        ArrayList<Product> usedProducts = new ArrayList();
        System.out.println("\u67e5\u627e\u5f00\u59cb");
        for (Material v_m : materials_index) {
            if (1 != v_m.getM_is_p_info()) continue;
            usedProducts = CommonTools.cloneProList(v_m.getM_products());
        }
        System.out.println(usedProducts.size());
        int i = 0;
        while (i < usedProducts.size()) {
            Product p_i = (Product)usedProducts.get(i);
            if (p_i.getP_is_score() == 0) {
                p_i.setP_p_count(1);
                int j = i + 1;
                while (j < usedProducts.size()) {
                    Product p_j = (Product)usedProducts.get(j);
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
                    ++j;
                }
            }
            ++i;
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
