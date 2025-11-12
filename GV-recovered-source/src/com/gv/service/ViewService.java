/*
 * Decompiled with CFR 0.152.
 */
package com.gv.service;

import com.gv.model.Material;
import com.gv.model.Product;
import com.gv.tool.CommonTools;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.Vector;

public class ViewService {
    public List<Material> createView(List<Product> m_products, List<Material> m_materials, double saw_bite) {
        ArrayList<Material> materials = new ArrayList<Material>();
        Product product = null;
        Material m_material = null;
        Map<String, List<Product>> m_products_map = this.processProduct(m_products);
        Map<String, List<Material>> m_materials_map = this.processMaterial(m_materials);
        Iterator<String> it = m_products_map.keySet().iterator();
        int p_count = 0;
        int m_m_no = 0;
        int m_p_no = 0;
        while (it.hasNext()) {
            String key = it.next();
            m_products = m_products_map.get(key);
            if ((m_products = this.scoreProduct(m_products, 0)).size() <= 0) continue;
            m_m_no = 0;
            m_p_no = 0;
            p_count = -1;
            m_materials = m_materials_map.get(key);
            if (m_materials != null) {
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
                    int j = 0;
                    while (j < m_products.size()) {
                        Product p = m_products.get(j);
                        if (!(m_material.getR_height() < p.getP_height()) && !(m_material.getR_width() < p.getP_width())) {
                            int node_id = 0;
                            p_count = (int)((m_material.getR_height() + saw_bite) / (p.getP_height() + saw_bite));
                            if (p_count == 0) {
                                System.out.println("\u4ea7\u54c1\u8fc7\u5927");
                            } else {
                                List vt_materials;
                                Iterator<Object> iterator;
                                Object vt_t;
                                m_p_no = j;
                                m_m_no = i;
                                product = m_products.get(m_p_no);
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
                                p.setM_left(12.0);
                                p.setM_top(12.0);
                                p.setP_name(product.getP_name());
                                p.setP_height(product.getP_height());
                                p.setP_width(product.getP_width());
                                p.setP_is_copy(product.getP_is_copy());
                                p.setP_is_dir(product.getP_is_dir());
                                p.setP_is_show(0);
                                m_ps.add(p);
                                p = null;
                                material.setM_products(m_ps);
                                product.setP_r_count(product.getP_r_count() - 1);
                                int index = 1;
                                TreeMap<String, List<Material>> t_materials_map = new TreeMap<String, List<Material>>();
                                TreeMap materials_map_index = new TreeMap();
                                TreeMap<Integer, Material> material_map = new TreeMap<Integer, Material>();
                                material_map.put(node_id, material);
                                Vector vt = new Vector();
                                ArrayList<Material> t_materials = null;
                                Material t_material = null;
                                t_materials = new ArrayList<Material>();
                                t_material = new Material();
                                t_material.setR_height(material.getR_height() - product.getP_height() - saw_bite);
                                t_material.setR_width(material.getR_width());
                                t_material.setM_width(material.getM_width());
                                t_material.setM_height(material.getM_height());
                                t_material.setM_f_id(material.getM_node_id());
                                t_material.setM_node_id(++node_id);
                                t_material.setM_c_type(0);
                                t_material.setM_hs_type(1);
                                t_material.setM_m_left(12.0);
                                t_material.setM_m_top(product.getP_height() + saw_bite + 12.0);
                                t_materials.add(t_material);
                                t_material = new Material();
                                t_material.setR_height(product.getP_height());
                                t_material.setR_width(material.getR_width() - product.getP_width() - saw_bite);
                                t_material.setM_width(material.getM_width());
                                t_material.setM_height(material.getM_height());
                                t_material.setM_f_id(material.getM_node_id());
                                t_material.setM_node_id(node_id);
                                t_material.setM_c_type(0);
                                t_material.setM_hs_type(0);
                                t_material.setM_m_left(product.getP_width() + saw_bite + 12.0);
                                t_material.setM_m_top(12.0);
                                t_materials.add(t_material);
                                t_materials_map.put("0", t_materials);
                                vt.add(t_materials);
                                t_materials = new ArrayList();
                                t_material = new Material();
                                t_material.setR_height(material.getR_height() - product.getP_height() - saw_bite);
                                t_material.setR_width(product.getP_width());
                                t_material.setM_width(material.getM_width());
                                t_material.setM_height(material.getM_height());
                                t_material.setM_f_id(material.getM_node_id());
                                t_material.setM_node_id(++node_id);
                                t_material.setM_c_type(1);
                                t_material.setM_hs_type(1);
                                t_material.setM_m_left(12.0);
                                t_material.setM_m_top(product.getP_height() + saw_bite + 12.0);
                                t_materials.add(t_material);
                                t_material = new Material();
                                t_material.setR_height(material.getR_height());
                                t_material.setR_width(material.getR_width() - product.getP_width() - saw_bite);
                                t_material.setM_width(material.getM_width());
                                t_material.setM_height(material.getM_height());
                                t_material.setM_f_id(material.getM_node_id());
                                t_material.setM_node_id(node_id);
                                t_material.setM_c_type(1);
                                t_material.setM_hs_type(0);
                                t_material.setM_m_left(product.getP_width() + saw_bite + 12.0);
                                t_material.setM_m_top(12.0);
                                t_materials.add(t_material);
                                t_materials_map.put("1", t_materials);
                                vt.add(t_materials);
                                material.setM_material_map(t_materials_map);
                                materials_map_index.put(index, vt);
                                Iterator it_t = materials_map_index.keySet().iterator();
                                while (it_t.hasNext()) {
                                    vt = (Vector)materials_map_index.get(index);
                                    Vector<ArrayList<Material>> vt_t2 = new Vector<ArrayList<Material>>();
                                    if (vt.size() == 0) break;
                                    for (List materials_index : vt) {
                                        block5: for (Material t_m : materials_index) {
                                            for (Product t_p : m_products) {
                                                if (t_p.getP_r_count() <= 0) continue;
                                                if (t_m.getR_width() == t_p.getP_width() && t_m.getR_height() == t_p.getP_height()) {
                                                    m_ps = new ArrayList();
                                                    p = new Product();
                                                    p.setM_left(t_m.getM_m_left());
                                                    p.setM_top(t_m.getM_m_top());
                                                    p.setP_name(t_p.getP_name());
                                                    p.setP_height(t_p.getP_height());
                                                    p.setP_width(t_p.getP_width());
                                                    p.setP_is_copy(t_p.getP_is_copy());
                                                    p.setP_is_dir(t_p.getP_is_dir());
                                                    p.setP_is_show(t_m.getM_node_id());
                                                    m_ps.add(p);
                                                    p = null;
                                                    t_m.setM_products(m_ps);
                                                    material_map.put(t_m.getM_node_id(), t_m);
                                                    t_materials = new ArrayList();
                                                    t_material = new Material();
                                                    t_material.setR_height(0.0);
                                                    t_material.setR_width(0.0);
                                                    t_material.setM_width(t_m.getM_width());
                                                    t_material.setM_height(t_m.getM_height());
                                                    t_material.setM_f_id(t_m.getM_node_id());
                                                    t_material.setM_node_id(++node_id);
                                                    t_material.setM_c_type(t_m.getM_c_type());
                                                    t_material.setM_hs_type(0);
                                                    t_material.setM_m_left(t_m.getM_m_left() + t_p.getP_width() + saw_bite);
                                                    t_material.setM_m_top(t_m.getM_m_top() + t_p.getP_height() + saw_bite);
                                                    t_materials.add(t_material);
                                                    t_materials_map.put("0", t_materials);
                                                    vt_t2.add(t_materials);
                                                    t_m.setM_material_map(t_materials_map);
                                                    continue block5;
                                                }
                                                if (t_m.getR_width() == t_p.getP_width() && t_m.getR_height() >= t_p.getP_height() + saw_bite) {
                                                    m_ps = new ArrayList();
                                                    p = new Product();
                                                    p.setM_left(t_m.getM_m_left());
                                                    p.setM_top(t_m.getM_m_top());
                                                    System.out.println(String.valueOf(p.getM_top()) + ":" + p.getM_left());
                                                    p.setP_name(t_p.getP_name());
                                                    p.setP_height(t_p.getP_height());
                                                    p.setP_width(t_p.getP_width());
                                                    p.setP_is_copy(t_p.getP_is_copy());
                                                    p.setP_is_dir(t_p.getP_is_dir());
                                                    p.setP_is_show(t_m.getM_node_id());
                                                    m_ps.add(p);
                                                    p = null;
                                                    t_m.setM_products(m_ps);
                                                    material_map.put(t_m.getM_node_id(), t_m);
                                                    t_materials = new ArrayList();
                                                    t_material = new Material();
                                                    t_material.setR_height(t_m.getR_height() - t_p.getP_height() - saw_bite);
                                                    t_material.setR_width(t_m.getR_width());
                                                    t_material.setM_width(t_m.getM_width());
                                                    t_material.setM_height(t_m.getM_height());
                                                    t_material.setM_f_id(t_m.getM_node_id());
                                                    t_material.setM_node_id(++node_id);
                                                    t_material.setM_c_type(t_m.getM_c_type());
                                                    t_material.setM_hs_type(1);
                                                    t_material.setM_m_left(t_m.getM_m_left());
                                                    t_material.setM_m_top(t_m.getM_m_top() + t_p.getP_height() + saw_bite);
                                                    t_materials.add(t_material);
                                                    t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                    vt_t2.add(t_materials);
                                                    t_m.setM_material_map(t_materials_map);
                                                    continue block5;
                                                }
                                                if (t_m.getR_width() >= t_p.getP_width() + saw_bite && t_m.getR_height() == t_p.getP_height()) {
                                                    m_ps = new ArrayList();
                                                    p = new Product();
                                                    p.setM_left(t_m.getM_m_left());
                                                    p.setM_top(t_m.getM_m_top());
                                                    System.out.println(String.valueOf(p.getM_top()) + ":" + p.getM_left());
                                                    p.setP_name(t_p.getP_name());
                                                    p.setP_height(t_p.getP_height());
                                                    p.setP_width(t_p.getP_width());
                                                    p.setP_is_copy(t_p.getP_is_copy());
                                                    p.setP_is_dir(t_p.getP_is_dir());
                                                    p.setP_is_show(t_m.getM_node_id());
                                                    m_ps.add(p);
                                                    p = null;
                                                    t_m.setM_products(m_ps);
                                                    material_map.put(t_m.getM_node_id(), t_m);
                                                    t_materials = new ArrayList();
                                                    t_material = new Material();
                                                    t_material.setR_height(t_m.getR_height());
                                                    t_material.setR_width(t_m.getR_width() - t_p.getP_width() - saw_bite);
                                                    t_material.setM_width(t_m.getM_width());
                                                    t_material.setM_height(t_m.getM_height());
                                                    t_material.setM_f_id(t_m.getM_node_id());
                                                    t_material.setM_node_id(++node_id);
                                                    t_material.setM_c_type(t_m.getM_c_type());
                                                    t_material.setM_hs_type(0);
                                                    t_material.setM_m_left(t_m.getM_m_left() + t_p.getP_width() + saw_bite);
                                                    t_material.setM_m_top(t_m.getM_m_top());
                                                    t_materials.add(t_material);
                                                    t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                    vt_t2.add(t_materials);
                                                    t_m.setM_material_map(t_materials_map);
                                                    continue block5;
                                                }
                                                if (!(t_m.getR_width() >= t_p.getP_width() + saw_bite) || !(t_m.getR_height() >= t_p.getP_height() + saw_bite)) continue;
                                                m_ps = new ArrayList();
                                                p = new Product();
                                                p.setM_left(t_m.getM_m_left());
                                                p.setM_top(t_m.getM_m_top());
                                                System.out.println(String.valueOf(p.getM_top()) + ":" + p.getM_left());
                                                p.setP_name(t_p.getP_name());
                                                p.setP_height(t_p.getP_height());
                                                p.setP_width(t_p.getP_width());
                                                p.setP_is_copy(t_p.getP_is_copy());
                                                p.setP_is_dir(t_p.getP_is_dir());
                                                p.setP_is_show(t_m.getM_node_id());
                                                m_ps.add(p);
                                                p = null;
                                                t_m.setM_products(m_ps);
                                                material_map.put(t_m.getM_node_id(), t_m);
                                                t_materials = new ArrayList();
                                                t_material = new Material();
                                                t_material.setR_height(t_m.getR_height() - t_p.getP_height() - saw_bite);
                                                t_material.setR_width(t_m.getR_width());
                                                t_material.setM_width(t_m.getM_width());
                                                t_material.setM_height(t_m.getM_height());
                                                t_material.setM_f_id(t_m.getM_node_id());
                                                t_material.setM_node_id(++node_id);
                                                t_material.setM_c_type(0);
                                                t_material.setM_hs_type(1);
                                                t_material.setM_m_left(t_m.getM_m_left());
                                                t_material.setM_m_top(t_m.getM_m_top() + t_p.getP_height() + saw_bite);
                                                t_materials.add(t_material);
                                                t_material = new Material();
                                                t_material.setR_height(t_p.getP_height());
                                                t_material.setR_width(t_m.getR_width() - t_p.getP_width() - saw_bite);
                                                t_material.setM_width(t_m.getM_width());
                                                t_material.setM_height(t_m.getM_height());
                                                t_material.setM_f_id(t_m.getM_node_id());
                                                t_material.setM_node_id(node_id);
                                                t_material.setM_c_type(0);
                                                t_material.setM_hs_type(0);
                                                t_material.setM_m_left(t_m.getM_m_left() + t_p.getP_width() + saw_bite);
                                                t_material.setM_m_top(t_m.getM_m_top());
                                                t_materials.add(t_material);
                                                t_materials_map.put("0", t_materials);
                                                vt_t2.add(t_materials);
                                                t_materials = new ArrayList();
                                                t_material = new Material();
                                                t_material.setR_height(t_m.getR_height() - t_p.getP_height() - saw_bite);
                                                t_material.setR_width(t_p.getP_width());
                                                t_material.setM_width(t_m.getM_width());
                                                t_material.setM_height(t_m.getM_height());
                                                t_material.setM_f_id(t_m.getM_node_id());
                                                t_material.setM_node_id(++node_id);
                                                t_material.setM_c_type(1);
                                                t_material.setM_hs_type(1);
                                                t_material.setM_m_left(t_m.getM_m_left());
                                                t_material.setM_m_top(t_m.getM_m_top() + t_p.getP_height() + saw_bite);
                                                t_materials.add(t_material);
                                                t_material = new Material();
                                                t_material.setR_height(t_m.getR_height());
                                                t_material.setR_width(t_m.getR_width() - t_p.getP_width() - saw_bite);
                                                t_material.setM_width(t_m.getM_width());
                                                t_material.setM_height(t_m.getM_height());
                                                t_material.setM_f_id(t_m.getM_node_id());
                                                t_material.setM_node_id(node_id);
                                                t_material.setM_c_type(1);
                                                t_material.setM_hs_type(0);
                                                t_material.setM_m_left(t_m.getM_m_left() + t_p.getP_width() + saw_bite);
                                                t_material.setM_m_top(t_m.getM_m_top());
                                                t_materials.add(t_material);
                                                t_materials_map.put("1", t_materials);
                                                vt_t2.add(t_materials);
                                                t_m.setM_material_map(t_materials_map);
                                                continue block5;
                                            }
                                        }
                                    }
                                    materials_map_index.put(++index, vt_t2);
                                    it_t = materials_map_index.keySet().iterator();
                                }
                                HashMap<String, Material> best_map = new HashMap<String, Material>();
                                b_material = new Material();
                                Iterator<String> b_it = null;
                                b_it = material.getM_material_map().keySet().iterator();
                                while (b_it.hasNext()) {
                                    b_material = CommonTools.cloneScheme(material);
                                    best_map.put(String.valueOf(material.getM_node_id()) + "-" + b_it.next(), b_material);
                                }
                                int i_i = 1;
                                while (i_i < index) {
                                    System.out.print("\u5c42\u6b21ID:" + i_i + ">>");
                                    vt_t = (Vector)materials_map_index.get(i_i);
                                    iterator = ((Vector)vt_t).iterator();
                                    while (iterator.hasNext()) {
                                        vt_materials = (List)iterator.next();
                                        System.out.print("[");
                                        for (Material vt_m : vt_materials) {
                                            System.out.println("ID:(" + vt_m.getM_node_id() + "),F_ID(" + vt_m.getM_f_id() + "),M_Left(" + vt_m.getM_m_left() + "),M_Top(" + vt_m.getM_m_top() + "),C_Type(" + vt_m.getM_c_type() + "),R_W(" + vt_m.getR_width() + "),R_H(" + vt_m.getR_height() + ")");
                                            System.out.print(vt_m.getM_products() + ",");
                                        }
                                        System.out.println("]");
                                    }
                                    ++i_i;
                                }
                                i_i = 1;
                                while (i_i < index) {
                                    vt_t = (Vector)materials_map_index.get(i_i);
                                    System.out.println("\u7b2c" + i_i + "\u5c42");
                                    System.out.println(best_map.keySet().size());
                                    iterator = ((Vector)vt_t).iterator();
                                    while (iterator.hasNext()) {
                                        vt_materials = (List)iterator.next();
                                        for (Material vt_m : vt_materials) {
                                            if (vt_m.getM_products() == null) continue;
                                            ((Material)best_map.get(String.valueOf(vt_m.getM_f_id()) + "-" + vt_m.getM_c_type())).getM_products().addAll(vt_m.getM_products());
                                        }
                                    }
                                    iterator = ((Vector)vt_t).iterator();
                                    while (iterator.hasNext()) {
                                        vt_materials = (List)iterator.next();
                                        for (Material vt_m : vt_materials) {
                                            t_material = (Material)best_map.get(String.valueOf(vt_m.getM_f_id()) + "-" + vt_m.getM_c_type());
                                            if (vt_m.getM_products() == null) continue;
                                            for (String t_key : vt_m.getM_material_map().keySet()) {
                                                t_material = CommonTools.cloneScheme(t_material);
                                                best_map.put(String.valueOf(vt_m.getM_node_id()) + "-" + t_key, t_material);
                                            }
                                        }
                                    }
                                    iterator = ((Vector)vt_t).iterator();
                                    while (iterator.hasNext()) {
                                        vt_materials = (List)iterator.next();
                                        for (Material vt_m : vt_materials) {
                                            if (vt_m.getM_products() == null || best_map.get(String.valueOf(vt_m.getM_f_id()) + "-" + vt_m.getM_c_type()) == null) continue;
                                            best_map.remove(String.valueOf(vt_m.getM_f_id()) + "-" + vt_m.getM_c_type());
                                        }
                                    }
                                    ++i_i;
                                }
                                b_it = best_map.keySet().iterator();
                                while (b_it.hasNext()) {
                                    b_material = (Material)best_map.get(b_it.next());
                                    for (Product p_p : b_material.getM_products()) {
                                        b_material.setM_area_used(b_material.getM_area_used() + p_p.getP_width() * p_p.getP_height());
                                    }
                                    b_material.setM_area_used(b_material.getM_area_used() / (b_material.getM_width() * b_material.getM_height()));
                                    System.out.println(b_material.getM_area_used());
                                }
                                String b_key = "";
                                b_it = best_map.keySet().iterator();
                                b_key = b_it.next();
                                String k = "";
                                while (b_it.hasNext()) {
                                    k = b_it.next();
                                    b_material = (Material)best_map.get(b_key);
                                    if (!(b_material.getM_area_used() < ((Material)best_map.get(k)).getM_area_used())) continue;
                                    b_key = k;
                                    b_material = (Material)best_map.get(b_key);
                                }
                                System.out.println("\u6700\u4f18\u89e3\u4ea7\u54c1\u6570\u91cf" + b_material.getM_products().size());
                                b_material = (Material)best_map.get(b_key);
                                for (Product p_p : b_material.getM_products()) {
                                    for (Product t_p : m_products) {
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
                                    }
                                }
                                int ll = 0;
                                while (ll < m_products.size()) {
                                    if (0.0 > m_products.get(ll).getP_count()) {
                                        System.out.println("\u6709\u4ea7\u54c1\u751f\u4ea7\u5b8c\u4e86");
                                        m_products.remove(ll);
                                        --ll;
                                    }
                                    ++ll;
                                }
                                materials.add(b_material);
                                if (m_products.size() <= 0) {
                                    System.out.println("\u6240\u6709\u4ea7\u54c1\u751f\u4ea7\u5b8c\u4e86\uff01");
                                    break;
                                }
                                --i;
                                j = m_products.size();
                            }
                        }
                        ++j;
                    }
                    ++i;
                }
            } else {
                System.out.println("\u6ca1\u6709\u9002\u5408\u7684\u677f\u6750");
                continue;
            }
            System.out.println("---------------");
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
        for (Material mm : materials) {
            System.out.println(mm.getM_node_id());
            for (Product pp : mm.getM_products()) {
                System.out.println(String.valueOf(pp.getP_is_show()) + "--Left:" + pp.getM_left() + ",Top" + pp.getM_top());
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

    public List<Product> scoreProduct(List<Product> products, int score_type) {
        LinkedList<Product> l_products = new LinkedList<Product>();
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
                            products.set(j, product);
                            product = t_product;
                        } else if (product.getP_height() == products.get(j).getP_height() && product.getP_width() < products.get(j).getP_width()) {
                            t_product = products.get(j);
                            products.set(j, product);
                            product = t_product;
                        }
                        ++j;
                    }
                    l_products.add(i, product);
                    ++i;
                }
                break;
            }
            case 1: {
                int i = 0;
                while (i < products.size()) {
                    Product product = products.get(i);
                    int j = i + 1;
                    while (j < products.size()) {
                        if (product.getP_width() < products.get(j).getP_width()) {
                            product = products.get(j);
                        } else if (product.getP_width() == products.get(j).getP_width() && product.getP_height() < products.get(j).getP_height()) {
                            product = products.get(j);
                        }
                        ++j;
                    }
                    l_products.add(i, product);
                    ++i;
                }
                break;
            }
        }
        return l_products;
    }
}
