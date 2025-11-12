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
import java.util.TreeMap;
import java.util.Vector;

public class CopyOfCopyOfCopyOfCopyOfViewService1 {
    public List<Material> createView(List<Product> m_products, List<Material> m_materials, double saw_bite) {
        ArrayList<Material> materials = null;
        ArrayList<Material> b_b_materials = new ArrayList<Material>();
        List b_materials = null;
        ArrayList<Material> i_materials = new ArrayList<Material>();
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
            b_materials = new ArrayList();
            Vector b_materials_vc = new Vector();
            int flag = 0;
            while (flag < 10) {
                materials = new ArrayList<Material>();
                List<Product> mm_products = this.scoreProduct(m_products, flag);
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
                                Product p = (Product)mm_products.get(j);
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
                                            Iterator<Object> iterator;
                                            m_m_no = i;
                                            product = (Product)mm_products.get(j);
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
                                            Iterator iterator2 = mm_products.iterator();
                                            while (iterator2.hasNext()) {
                                                Product t_p = (Product)iterator2.next();
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
                                            t_materials = new ArrayList<Material>();
                                            t_material = new Material();
                                            t_material.setR_height(DecimalMath.mul(DecimalMath.mul(material.getR_height(), product.getP_height()), saw_bite));
                                            t_material.setR_width(material.getR_width());
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_node_id(++node_id);
                                            t_material.setM_c_type(0);
                                            t_material.setM_hs_type(1);
                                            t_material.setM_m_left(0.0);
                                            t_material.setM_m_top(product.getP_height() + saw_bite);
                                            t_materials.add(t_material);
                                            t_material = new Material();
                                            t_material.setR_height(product.getP_height());
                                            t_material.setR_width(DecimalMath.mul(DecimalMath.mul(material.getR_width(), product.getP_width()), saw_bite));
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_node_id(node_id);
                                            t_material.setM_c_type(0);
                                            t_material.setM_hs_type(0);
                                            t_material.setM_m_left(product.getP_width() + saw_bite);
                                            t_material.setM_m_top(0.0);
                                            t_materials.add(t_material);
                                            t_materials_map.put("0", t_materials);
                                            vt.add(t_materials);
                                            t_materials = new ArrayList();
                                            t_material = new Material();
                                            t_material.setR_height(DecimalMath.mul(DecimalMath.mul(material.getR_height(), product.getP_height()), saw_bite));
                                            t_material.setR_width(product.getP_width());
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_node_id(++node_id);
                                            t_material.setM_c_type(1);
                                            t_material.setM_hs_type(1);
                                            t_material.setM_m_left(0.0);
                                            t_material.setM_m_top(product.getP_height() + saw_bite);
                                            t_materials.add(t_material);
                                            t_material = new Material();
                                            t_material.setR_height(material.getR_height());
                                            t_material.setR_width(DecimalMath.mul(DecimalMath.mul(material.getR_width(), product.getP_width()), saw_bite));
                                            t_material.setM_width(material.getM_width());
                                            t_material.setM_height(material.getM_height());
                                            t_material.setM_f_id(material.getM_node_id());
                                            t_material.setM_node_id(node_id);
                                            t_material.setM_c_type(1);
                                            t_material.setM_hs_type(0);
                                            t_material.setM_m_left(product.getP_width() + saw_bite);
                                            t_material.setM_m_top(0.0);
                                            t_materials.add(t_material);
                                            t_materials_map.put("1", t_materials);
                                            vt.add(t_materials);
                                            material.setM_material_map(t_materials_map);
                                            materials_map_index.put(index, vt);
                                            Iterator it_t = materials_map_index.keySet().iterator();
                                            while (it_t.hasNext()) {
                                                vt = (Vector)materials_map_index.get(index);
                                                Vector<ArrayList<Material>> vt_t = new Vector<ArrayList<Material>>();
                                                if (vt.size() == 0) break;
                                                for (List materials_index : vt) {
                                                    block7: for (Material t_m : materials_index) {
                                                        Iterator iterator3 = mm_products.iterator();
                                                        while (iterator3.hasNext()) {
                                                            int pj;
                                                            int pi;
                                                            Object b_product2;
                                                            Product b_product1;
                                                            Product pppp;
                                                            double mod;
                                                            double m_mod;
                                                            int pp_count;
                                                            Product t_p = (Product)iterator3.next();
                                                            ArrayList<Product> e_products = null;
                                                            if (t_p.getP_r_count() <= 0) continue;
                                                            if (t_m.getR_width() == t_p.getP_width() && t_m.getR_height() == t_p.getP_height()) {
                                                                m_ps = new ArrayList();
                                                                p = new Product();
                                                                p.setM_left(t_m.getM_m_left());
                                                                p.setM_top(t_m.getM_m_top());
                                                                p.setP_no(t_p.getP_no());
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
                                                                t_material.setM_m_left(DecimalMath.add(DecimalMath.add(t_m.getM_m_left(), t_p.getP_width()), saw_bite));
                                                                t_material.setM_m_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), t_p.getP_height()), saw_bite));
                                                                t_materials.add(t_material);
                                                                t_materials_map.put("0", t_materials);
                                                                vt_t.add(t_materials);
                                                                t_m.setM_material_map(t_materials_map);
                                                                continue block7;
                                                            }
                                                            if (t_m.getR_width() == t_p.getP_width() && t_m.getR_height() >= t_p.getP_height() + saw_bite) {
                                                                pp_count = (int)(t_m.getR_height() / t_p.getP_height());
                                                                m_mod = 100000.0;
                                                                mod = 0.0;
                                                                e_products = new ArrayList<Product>();
                                                                if (1 == pp_count) {
                                                                    m_mod = t_m.getR_height() - t_p.getP_height() - saw_bite;
                                                                    Iterator iterator4 = mm_products.iterator();
                                                                    while (iterator4.hasNext()) {
                                                                        pppp = (Product)iterator4.next();
                                                                        if (pppp.getP_r_count() <= 0 || pppp.getP_width() != t_p.getP_width() || pppp.getP_height() == t_p.getP_height()) continue;
                                                                        e_products.add(pppp);
                                                                    }
                                                                    b_product1 = null;
                                                                    b_product2 = null;
                                                                    pi = 0;
                                                                    while (pi < e_products.size()) {
                                                                        pj = e_products.size() - 1;
                                                                        while (pj > pi) {
                                                                            mod = t_m.getR_height() - ((Product)e_products.get(pi)).getP_height() - ((Product)e_products.get(pj)).getP_height() - saw_bite;
                                                                            if (mod >= 0.0 && mod < m_mod) {
                                                                                b_product1 = (Product)e_products.get(pi);
                                                                                b_product2 = (Product)e_products.get(pj);
                                                                                m_mod = mod;
                                                                            }
                                                                            --pj;
                                                                        }
                                                                        ++pi;
                                                                    }
                                                                    if (b_product1 != null && b_product2 != null) {
                                                                        m_ps = new ArrayList();
                                                                        p = new Product();
                                                                        p.setM_left(t_m.getM_m_left());
                                                                        p.setM_top(t_m.getM_m_top());
                                                                        p.setP_no(b_product1.getP_no());
                                                                        p.setP_name(b_product1.getP_name());
                                                                        p.setP_height(b_product1.getP_height());
                                                                        p.setP_width(b_product1.getP_width());
                                                                        p.setP_is_copy(b_product1.getP_is_copy());
                                                                        p.setP_is_dir(b_product1.getP_is_dir());
                                                                        p.setP_is_show(t_m.getM_node_id());
                                                                        m_ps.add(p);
                                                                        p = null;
                                                                        p = new Product();
                                                                        p.setM_left(t_m.getM_m_left());
                                                                        p.setM_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), b_product1.getP_height()), saw_bite));
                                                                        p.setP_no(((Product)b_product2).getP_no());
                                                                        p.setP_name(((Product)b_product2).getP_name());
                                                                        p.setP_height(((Product)b_product2).getP_height());
                                                                        p.setP_width(((Product)b_product2).getP_width());
                                                                        p.setP_is_copy(((Product)b_product2).getP_is_copy());
                                                                        p.setP_is_dir(((Product)b_product2).getP_is_dir());
                                                                        p.setP_is_show(t_m.getM_node_id());
                                                                        m_ps.add(p);
                                                                        p = null;
                                                                        t_m.setM_products(m_ps);
                                                                        material_map.put(t_m.getM_node_id(), t_m);
                                                                        t_materials = new ArrayList();
                                                                        t_material = new Material();
                                                                        t_material.setR_height(DecimalMath.mul(DecimalMath.mul(t_m.getR_height(), ((Product)b_product2).getP_height()), DecimalMath.mul(b_product1.getP_height(), DecimalMath.sub(2.0, saw_bite))));
                                                                        t_material.setR_width(t_m.getR_width());
                                                                        t_material.setM_width(t_m.getM_width());
                                                                        t_material.setM_height(t_m.getM_height());
                                                                        t_material.setM_f_id(t_m.getM_node_id());
                                                                        t_material.setM_node_id(++node_id);
                                                                        t_material.setM_c_type(t_m.getM_c_type());
                                                                        t_material.setM_hs_type(1);
                                                                        t_material.setM_m_left(t_m.getM_m_left());
                                                                        t_material.setM_m_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), ((Product)b_product2).getP_height()), DecimalMath.add(b_product1.getP_height(), DecimalMath.sub(2.0, saw_bite))));
                                                                        t_materials.add(t_material);
                                                                        t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                                        vt_t.add(t_materials);
                                                                        t_m.setM_material_map(t_materials_map);
                                                                        continue block7;
                                                                    }
                                                                    m_ps = new ArrayList();
                                                                    p = new Product();
                                                                    p.setM_left(t_m.getM_m_left());
                                                                    p.setM_top(t_m.getM_m_top());
                                                                    p.setP_no(t_p.getP_no());
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
                                                                    t_material.setR_height(DecimalMath.mul(DecimalMath.mul(t_m.getR_height(), t_p.getP_height()), saw_bite));
                                                                    t_material.setR_width(t_m.getR_width());
                                                                    t_material.setM_width(t_m.getM_width());
                                                                    t_material.setM_height(t_m.getM_height());
                                                                    t_material.setM_f_id(t_m.getM_node_id());
                                                                    t_material.setM_node_id(++node_id);
                                                                    t_material.setM_c_type(t_m.getM_c_type());
                                                                    t_material.setM_hs_type(1);
                                                                    t_material.setM_m_left(t_m.getM_m_left());
                                                                    t_material.setM_m_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), t_p.getP_height()), saw_bite));
                                                                    t_materials.add(t_material);
                                                                    t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                                    vt_t.add(t_materials);
                                                                    t_m.setM_material_map(t_materials_map);
                                                                    continue block7;
                                                                }
                                                                m_ps = new ArrayList();
                                                                p = new Product();
                                                                p.setM_left(t_m.getM_m_left());
                                                                p.setM_top(t_m.getM_m_top());
                                                                p.setP_no(t_p.getP_no());
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
                                                                t_material.setR_height(DecimalMath.mul(DecimalMath.mul(t_m.getR_height(), t_p.getP_height()), saw_bite));
                                                                t_material.setR_width(t_m.getR_width());
                                                                t_material.setM_width(t_m.getM_width());
                                                                t_material.setM_height(t_m.getM_height());
                                                                t_material.setM_f_id(t_m.getM_node_id());
                                                                t_material.setM_node_id(++node_id);
                                                                t_material.setM_c_type(t_m.getM_c_type());
                                                                t_material.setM_hs_type(1);
                                                                t_material.setM_m_left(t_m.getM_m_left());
                                                                t_material.setM_m_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), t_p.getP_height()), saw_bite));
                                                                t_materials.add(t_material);
                                                                t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                                vt_t.add(t_materials);
                                                                t_m.setM_material_map(t_materials_map);
                                                                continue block7;
                                                            }
                                                            if (t_m.getR_width() >= t_p.getP_width() + saw_bite && t_m.getR_height() == t_p.getP_height()) {
                                                                pp_count = (int)(t_m.getR_width() / t_p.getP_width());
                                                                m_mod = 100000.0;
                                                                mod = 0.0;
                                                                e_products = new ArrayList();
                                                                if (1 == pp_count) {
                                                                    m_mod = t_m.getR_width() - t_p.getP_width() - saw_bite;
                                                                    b_product2 = mm_products.iterator();
                                                                    while (b_product2.hasNext()) {
                                                                        pppp = (Product)b_product2.next();
                                                                        if (pppp.getP_r_count() <= 0 || pppp.getP_height() != t_p.getP_height() || pppp.getP_width() == t_p.getP_width()) continue;
                                                                        e_products.add(pppp);
                                                                    }
                                                                    b_product1 = null;
                                                                    b_product2 = null;
                                                                    pi = 0;
                                                                    while (pi < e_products.size()) {
                                                                        pj = e_products.size() - 1;
                                                                        while (pj > pi) {
                                                                            mod = t_m.getR_width() - ((Product)e_products.get(pi)).getP_width() - ((Product)e_products.get(pj)).getP_width() - saw_bite;
                                                                            if (mod >= 0.0 && mod < m_mod) {
                                                                                b_product1 = (Product)e_products.get(pi);
                                                                                b_product2 = (Product)e_products.get(pj);
                                                                                m_mod = mod;
                                                                            }
                                                                            --pj;
                                                                        }
                                                                        ++pi;
                                                                    }
                                                                    if (b_product1 != null && b_product2 != null) {
                                                                        m_ps = new ArrayList();
                                                                        p = new Product();
                                                                        p.setM_left(t_m.getM_m_left());
                                                                        p.setM_top(t_m.getM_m_top());
                                                                        p.setP_no(b_product1.getP_no());
                                                                        p.setP_name(b_product1.getP_name());
                                                                        p.setP_height(b_product1.getP_height());
                                                                        p.setP_width(b_product1.getP_width());
                                                                        p.setP_is_copy(b_product1.getP_is_copy());
                                                                        p.setP_is_dir(b_product1.getP_is_dir());
                                                                        p.setP_is_show(t_m.getM_node_id());
                                                                        m_ps.add(p);
                                                                        p = null;
                                                                        p = new Product();
                                                                        p.setM_left(DecimalMath.add(DecimalMath.add(t_m.getM_m_left(), b_product1.getP_width()), saw_bite));
                                                                        p.setM_top(t_m.getM_m_top());
                                                                        p.setP_no(((Product)b_product2).getP_no());
                                                                        p.setP_name(((Product)b_product2).getP_name());
                                                                        p.setP_height(((Product)b_product2).getP_height());
                                                                        p.setP_width(((Product)b_product2).getP_width());
                                                                        p.setP_is_copy(((Product)b_product2).getP_is_copy());
                                                                        p.setP_is_dir(((Product)b_product2).getP_is_dir());
                                                                        p.setP_is_show(t_m.getM_node_id());
                                                                        m_ps.add(p);
                                                                        p = null;
                                                                        t_m.setM_products(m_ps);
                                                                        material_map.put(t_m.getM_node_id(), t_m);
                                                                        t_materials = new ArrayList();
                                                                        t_material = new Material();
                                                                        t_material.setR_height(t_m.getR_height());
                                                                        t_material.setR_width(DecimalMath.mul(DecimalMath.mul(t_m.getR_width(), b_product1.getP_width()), DecimalMath.mul(((Product)b_product2).getP_width(), DecimalMath.sub(2.0, saw_bite))));
                                                                        t_material.setM_width(t_m.getM_width());
                                                                        t_material.setM_height(t_m.getM_height());
                                                                        t_material.setM_f_id(t_m.getM_node_id());
                                                                        t_material.setM_node_id(++node_id);
                                                                        t_material.setM_c_type(t_m.getM_c_type());
                                                                        t_material.setM_hs_type(1);
                                                                        t_material.setM_m_left(DecimalMath.add(DecimalMath.add(t_m.getM_m_left(), b_product1.getP_width()), DecimalMath.add(((Product)b_product2).getP_width(), DecimalMath.sub(2.0, saw_bite))));
                                                                        t_material.setM_m_top(t_m.getM_m_top());
                                                                        t_materials.add(t_material);
                                                                        t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                                        vt_t.add(t_materials);
                                                                        t_m.setM_material_map(t_materials_map);
                                                                        continue block7;
                                                                    }
                                                                    m_ps = new ArrayList();
                                                                    p = new Product();
                                                                    p.setM_left(t_m.getM_m_left());
                                                                    p.setM_top(t_m.getM_m_top());
                                                                    System.out.println(String.valueOf(p.getM_top()) + ":" + p.getM_left());
                                                                    p.setP_no(t_p.getP_no());
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
                                                                    t_material.setR_width(DecimalMath.mul(DecimalMath.mul(t_m.getR_width(), t_p.getP_width()), saw_bite));
                                                                    t_material.setM_width(t_m.getM_width());
                                                                    t_material.setM_height(t_m.getM_height());
                                                                    t_material.setM_f_id(t_m.getM_node_id());
                                                                    t_material.setM_node_id(++node_id);
                                                                    t_material.setM_c_type(t_m.getM_c_type());
                                                                    t_material.setM_hs_type(0);
                                                                    t_material.setM_m_left(DecimalMath.add(DecimalMath.add(t_m.getM_m_left(), t_p.getP_width()), saw_bite));
                                                                    t_material.setM_m_top(t_m.getM_m_top());
                                                                    t_materials.add(t_material);
                                                                    t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                                    vt_t.add(t_materials);
                                                                    t_m.setM_material_map(t_materials_map);
                                                                    continue block7;
                                                                }
                                                                m_ps = new ArrayList();
                                                                p = new Product();
                                                                p.setM_left(t_m.getM_m_left());
                                                                p.setM_top(t_m.getM_m_top());
                                                                System.out.println(String.valueOf(p.getM_top()) + ":" + p.getM_left());
                                                                p.setP_no(t_p.getP_no());
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
                                                                t_material.setR_width(DecimalMath.mul(DecimalMath.mul(t_m.getR_width(), t_p.getP_width()), saw_bite));
                                                                t_material.setM_width(t_m.getM_width());
                                                                t_material.setM_height(t_m.getM_height());
                                                                t_material.setM_f_id(t_m.getM_node_id());
                                                                t_material.setM_node_id(++node_id);
                                                                t_material.setM_c_type(t_m.getM_c_type());
                                                                t_material.setM_hs_type(0);
                                                                t_material.setM_m_left(DecimalMath.add(DecimalMath.add(t_m.getM_m_left(), t_p.getP_width()), saw_bite));
                                                                t_material.setM_m_top(t_m.getM_m_top());
                                                                t_materials.add(t_material);
                                                                t_materials_map.put(String.valueOf(t_material.getM_c_type()), t_materials);
                                                                vt_t.add(t_materials);
                                                                t_m.setM_material_map(t_materials_map);
                                                                continue block7;
                                                            }
                                                            if (!(t_m.getR_width() >= t_p.getP_width() + saw_bite) || !(t_m.getR_height() >= t_p.getP_height() + saw_bite)) continue;
                                                            m_ps = new ArrayList();
                                                            p = new Product();
                                                            p.setM_left(t_m.getM_m_left());
                                                            p.setM_top(t_m.getM_m_top());
                                                            System.out.println(String.valueOf(p.getM_top()) + ":" + p.getM_left());
                                                            p.setP_no(t_p.getP_no());
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
                                                            t_material.setR_height(DecimalMath.mul(DecimalMath.mul(t_m.getR_height(), t_p.getP_height()), saw_bite));
                                                            t_material.setR_width(t_m.getR_width());
                                                            t_material.setM_width(t_m.getM_width());
                                                            t_material.setM_height(t_m.getM_height());
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_node_id(++node_id);
                                                            t_material.setM_c_type(0);
                                                            t_material.setM_hs_type(1);
                                                            t_material.setM_m_left(t_m.getM_m_left());
                                                            t_material.setM_m_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), t_p.getP_height()), saw_bite));
                                                            t_materials.add(t_material);
                                                            t_material = new Material();
                                                            t_material.setR_height(t_p.getP_height());
                                                            t_material.setR_width(DecimalMath.mul(DecimalMath.mul(t_m.getR_width(), t_p.getP_width()), saw_bite));
                                                            t_material.setM_width(t_m.getM_width());
                                                            t_material.setM_height(t_m.getM_height());
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_node_id(node_id);
                                                            t_material.setM_c_type(0);
                                                            t_material.setM_hs_type(0);
                                                            t_material.setM_m_left(DecimalMath.add(DecimalMath.add(t_m.getM_m_left(), t_p.getP_width()), saw_bite));
                                                            t_material.setM_m_top(t_m.getM_m_top());
                                                            t_materials.add(t_material);
                                                            t_materials_map.put("0", t_materials);
                                                            vt_t.add(t_materials);
                                                            t_materials = new ArrayList();
                                                            t_material = new Material();
                                                            t_material.setR_height(DecimalMath.mul(DecimalMath.mul(t_m.getR_height(), t_p.getP_height()), saw_bite));
                                                            t_material.setR_width(t_p.getP_width());
                                                            t_material.setM_width(t_m.getM_width());
                                                            t_material.setM_height(t_m.getM_height());
                                                            t_material.setM_f_id(t_m.getM_node_id());
                                                            t_material.setM_node_id(++node_id);
                                                            t_material.setM_c_type(1);
                                                            t_material.setM_hs_type(1);
                                                            t_material.setM_m_left(t_m.getM_m_left());
                                                            t_material.setM_m_top(DecimalMath.add(DecimalMath.add(t_m.getM_m_top(), t_p.getP_height()), saw_bite));
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
                                                            vt_t.add(t_materials);
                                                            t_m.setM_material_map(t_materials_map);
                                                            continue block7;
                                                        }
                                                    }
                                                }
                                                materials_map_index.put(++index, vt_t);
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
                                                List vt_materials;
                                                Vector vt_t = (Vector)materials_map_index.get(i_i);
                                                System.out.println("\u7b2c" + i_i + "\u5c42");
                                                System.out.println(best_map.keySet().size());
                                                iterator = vt_t.iterator();
                                                while (iterator.hasNext()) {
                                                    vt_materials = (List)iterator.next();
                                                    for (Material vt_m : vt_materials) {
                                                        if (vt_m.getM_products() == null) continue;
                                                        ((Material)best_map.get(String.valueOf(vt_m.getM_f_id()) + "-" + vt_m.getM_c_type())).getM_products().addAll(vt_m.getM_products());
                                                    }
                                                }
                                                iterator = vt_t.iterator();
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
                                                iterator = vt_t.iterator();
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
                                            Object b_key = "";
                                            b_it = best_map.keySet().iterator();
                                            b_key = b_it.next();
                                            Object k = "";
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
                                                Iterator iterator5 = mm_products.iterator();
                                                while (iterator5.hasNext()) {
                                                    Product t_p = (Product)iterator5.next();
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
                                            iterator = mm_products.iterator();
                                            while (iterator.hasNext()) {
                                                Product t_p = (Product)iterator.next();
                                                t_p.setP_r_count((int)t_p.getP_count());
                                            }
                                            int ll = 0;
                                            while (ll < mm_products.size()) {
                                                if (0.0 >= ((Product)mm_products.get(ll)).getP_count()) {
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
            b_materials = (List)b_materials_vc.get(0);
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
                List<Material> m_y_materials = new ArrayList<Material>();
                for (Product ppp : mm.getM_products()) {
                    boolean ft;
                    double ll;
                    Object y_m;
                    boolean fl;
                    double tt;
                    Object m_y2;
                    Object m_y1;
                    double t_point;
                    double l_point;
                    block133: {
                        block132: {
                            l_point = ppp.getM_left() + ppp.getP_width() + saw_bite;
                            t_point = ppp.getM_top() + ppp.getP_height() + saw_bite;
                            boolean l = false;
                            boolean t = false;
                            boolean d = false;
                            m_y1 = null;
                            m_y2 = null;
                            for (Product pppp : mm.getM_products()) {
                                if (l_point == pppp.getM_left() && (ppp.getM_top() == pppp.getM_top() || ppp.getM_top() >= pppp.getM_top())) {
                                    l = true;
                                } else if (t_point == pppp.getM_top() && ppp.getM_left() >= pppp.getM_left() && ppp.getM_left() <= pppp.getM_left() + pppp.getP_width()) {
                                    t = true;
                                }
                                if (!(l_point == pppp.getM_left() && t_point == pppp.getM_top() || l_point == pppp.getM_left() && t_point >= pppp.getM_top() && t_point <= pppp.getM_top() + pppp.getP_height()) && (t_point != pppp.getM_top() || !(l_point >= pppp.getM_left()) || !(l_point <= pppp.getM_left() + pppp.getP_width()))) continue;
                                d = true;
                            }
                            if (!l) {
                                boolean ft2;
                                double ll2;
                                block129: {
                                    block128: {
                                        ll2 = l_point;
                                        tt = ppp.getM_top();
                                        fl = false;
                                        do {
                                            if (ll2 < mm.getM_width()) {
                                                ll2 = DecimalMath.add(ll2, 0.5);
                                            }
                                            for (Product pppp : mm.getM_products()) {
                                                if (pppp.getM_left() == ll2 && tt >= pppp.getM_top() && tt <= pppp.getM_top() + pppp.getP_height()) {
                                                    fl = true;
                                                    break;
                                                }
                                                if (pppp.getM_left() != ll2 || tt != pppp.getM_top() + pppp.getP_height() + saw_bite) continue;
                                                fl = true;
                                                break;
                                            }
                                            if (fl) break block128;
                                        } while (!(ll2 >= mm.getM_width()));
                                        fl = true;
                                    }
                                    ft2 = false;
                                    do {
                                        if (tt < ppp.getP_height()) {
                                            tt = DecimalMath.add(tt, 0.5);
                                        }
                                        for (Product pppp : mm.getM_products()) {
                                            if (pppp.getM_top() == tt && l_point <= pppp.getM_left() + pppp.getP_width() && l_point >= pppp.getM_left()) {
                                                System.out.println("sssssssssssssssss");
                                                ft2 = true;
                                                break;
                                            }
                                            if (pppp.getM_top() != tt || !(ll2 < pppp.getM_left())) continue;
                                            ft2 = true;
                                            break;
                                        }
                                        if (ft2) break block129;
                                    } while (!(tt >= ppp.getP_height()));
                                    ft2 = true;
                                }
                                if (ft2 && fl) {
                                    y_m = new Material();
                                    ((Material)y_m).setM_width(mm.getM_width());
                                    ((Material)y_m).setM_height(mm.getM_height());
                                    if (ll2 == mm.getM_width()) {
                                        ((Material)y_m).setR_width(DecimalMath.mul(ll2, l_point) - 6.0);
                                    } else {
                                        ((Material)y_m).setR_width(DecimalMath.mul(ll2, l_point) - 4.0);
                                    }
                                    if (tt == mm.getM_height()) {
                                        if (0.0 == ppp.getM_top()) {
                                            ((Material)y_m).setR_height(DecimalMath.mul(tt, ppp.getM_top()) - 6.0);
                                        } else {
                                            ((Material)y_m).setR_height(DecimalMath.mul(tt, ppp.getM_top()) - 10.0);
                                        }
                                    } else {
                                        ((Material)y_m).setR_height(ppp.getP_height());
                                    }
                                    ((Material)y_m).setM_m_left(l_point);
                                    ((Material)y_m).setM_m_top(ppp.getM_top());
                                    ((Material)y_m).setM_y_is_ud(0);
                                    m_y_materials.add((Material)y_m);
                                    m_y1 = y_m;
                                }
                            }
                            if (!t) {
                                boolean ft3;
                                double ll3;
                                block131: {
                                    block130: {
                                        ll3 = ppp.getM_left();
                                        tt = t_point;
                                        fl = false;
                                        do {
                                            if (ll3 < ppp.getM_left() + ppp.getP_width()) {
                                                ll3 = DecimalMath.add(ll3, 0.5);
                                            }
                                            for (Product pppp : mm.getM_products()) {
                                                if (pppp.getM_left() != ll3 || !(tt >= pppp.getM_top()) || !(tt <= pppp.getM_top() + pppp.getP_height())) continue;
                                                fl = true;
                                                break;
                                            }
                                            if (fl) break block130;
                                        } while (!(ll3 >= ppp.getM_left() + ppp.getP_width()));
                                        fl = true;
                                    }
                                    ft3 = false;
                                    do {
                                        if (tt < mm.getM_height()) {
                                            tt = DecimalMath.add(tt, 0.5);
                                        }
                                        for (Product pppp : mm.getM_products()) {
                                            if (pppp.getM_top() != tt || !(ppp.getM_left() >= pppp.getM_left()) || !(ppp.getM_left() <= pppp.getM_left() + pppp.getP_width())) continue;
                                            ft3 = true;
                                            break;
                                        }
                                        if (ft3) break block131;
                                    } while (!(tt >= mm.getM_height()));
                                    ft3 = true;
                                }
                                if (fl && ft3) {
                                    y_m = new Material();
                                    ((Material)y_m).setM_width(mm.getM_width());
                                    ((Material)y_m).setM_height(mm.getM_height());
                                    ((Material)y_m).setR_width(DecimalMath.mul(ll3, ppp.getM_left()));
                                    if (tt == mm.getM_height()) {
                                        ((Material)y_m).setR_height(DecimalMath.mul(tt, t_point) - 6.0);
                                    } else {
                                        ((Material)y_m).setR_height(DecimalMath.mul(tt, t_point) - 8.0);
                                    }
                                    ((Material)y_m).setM_m_left(ppp.getM_left());
                                    ((Material)y_m).setM_m_top(t_point);
                                    ((Material)y_m).setM_y_is_ud(1);
                                    m_y_materials.add((Material)y_m);
                                    m_y2 = y_m;
                                }
                            }
                            if (d || l || t) continue;
                            ll = l_point;
                            tt = t_point;
                            fl = false;
                            do {
                                if (ll < mm.getM_width()) {
                                    ll = DecimalMath.add(ll, 0.5);
                                }
                                for (Product pppp : mm.getM_products()) {
                                    if (pppp.getM_left() == ll && tt >= pppp.getM_top() && tt <= pppp.getM_top() + pppp.getP_height()) {
                                        fl = true;
                                        break;
                                    }
                                    if (pppp.getM_left() != ll || !(tt >= pppp.getM_top() + pppp.getP_height())) continue;
                                    fl = true;
                                    break;
                                }
                                if (fl) break block132;
                            } while (!(ll >= mm.getM_width()));
                            fl = true;
                        }
                        ft = false;
                        do {
                            if (tt < mm.getM_height()) {
                                tt = DecimalMath.add(tt, 0.5);
                            }
                            for (Product pppp : mm.getM_products()) {
                                if (pppp.getM_top() != tt || !(ppp.getM_left() >= pppp.getM_left()) || !(ppp.getM_left() <= pppp.getM_left() + pppp.getP_width())) continue;
                                ft = true;
                                break;
                            }
                            if (ft) break block133;
                        } while (!(tt >= mm.getM_height()));
                        ft = true;
                    }
                    if (!fl || !ft) continue;
                    y_m = new Material();
                    ((Material)y_m).setM_width(mm.getM_width());
                    ((Material)y_m).setM_height(mm.getM_height());
                    ((Material)y_m).setR_width(DecimalMath.mul(ll, l_point));
                    if (tt == mm.getM_height()) {
                        ((Material)y_m).setR_height(DecimalMath.mul(tt, t_point) - 6.0);
                    } else {
                        ((Material)y_m).setR_height(DecimalMath.mul(tt, t_point) - 8.0);
                    }
                    ((Material)y_m).setM_m_left(l_point);
                    ((Material)y_m).setM_m_top(t_point);
                    ((Material)y_m).setM_y_is_ud(2);
                    double s1 = ((Material)m_y1).getR_height() * ((Material)m_y1).getR_width();
                    double s2 = ((Material)m_y2).getR_height() * ((Material)m_y2).getR_width();
                    Object b_m_y = null;
                    b_m_y = s1 >= s2 ? m_y1 : m_y2;
                    System.out.println(b_m_y);
                    if (((Material)b_m_y).getM_m_left() < ((Material)y_m).getM_m_left()) {
                        ((Material)b_m_y).setR_width(((Material)b_m_y).getR_width() + saw_bite + ((Material)y_m).getR_width());
                        continue;
                    }
                    ((Material)b_m_y).setR_height(((Material)b_m_y).getR_height() + saw_bite + ((Material)y_m).getR_height());
                }
                System.out.println("\u4f59\u6599\u6570\u91cf\uff1a" + m_y_materials.size());
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
                m_y_materials = this.scoreYMaterials(m_y_materials);
                int y_i = 0;
                while (y_i < m_y_materials.size()) {
                    if (1 == m_y_materials.get(y_i).getM_is_show()) {
                        m_y_materials.remove(y_i);
                        --y_i;
                    }
                    ++y_i;
                }
                mm.setM_y_materials(m_y_materials);
                for (Material y_m : m_y_materials) {
                    System.out.println("Type :" + y_m.getM_y_is_ud() + "T" + y_m.getM_m_left() + ":" + "L" + y_m.getM_m_top() + "(" + y_m.getR_width() + "*" + y_m.getR_height() + ")");
                }
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
            Material i_material = null;
            for (Material i_m : b_materials) {
                if (i_m.getM_is_yl() != 0) continue;
                i_material = CommonTools.cloneScheme(i_m);
                i_material.setM_u_count(0);
                break;
            }
            for (Material i_m : b_materials) {
                if (i_m.getM_is_yl() != 0) continue;
                i_material.setM_u_count(i_material.getM_u_count() + 1);
            }
            System.out.println("\u5171\u4f7f\u7528" + i_material.getM_width() + " * " + i_material.getM_height() + " - " + i_material.getM_u_count());
            i_materials.add(i_material);
            b_b_materials.addAll(b_materials);
        }
        Material i_material = null;
        for (Material i_m : b_materials) {
            if (i_m.getM_is_yl() != 0) continue;
            i_material = CommonTools.cloneScheme(i_m);
            i_material.setM_u_count(0);
            break;
        }
        for (Material i_m : b_materials) {
            if (i_m.getM_is_yl() != 0) continue;
            i_material.setM_u_count(i_material.getM_u_count() + 1);
        }
        System.out.println("\u5171\u4f7f\u7528" + i_material.getM_width() + " * " + i_material.getM_height() + " - " + i_material.getM_u_count());
        i_materials.add(i_material);
        b_b_materials.addAll(b_materials);
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
        List<Product> l_products = CommonTools.cloneProList(products);
        Product t_product = null;
        switch (score_type) {
            case 0: {
                int i = 0;
                while (i < l_products.size()) {
                    Product product = l_products.get(i);
                    int j = i + 1;
                    while (j < l_products.size()) {
                        if (product.getP_height() < l_products.get(j).getP_height()) {
                            t_product = l_products.get(j);
                            l_products.set(i, t_product);
                            l_products.set(j, product);
                            product = l_products.get(i);
                        } else if (product.getP_height() == l_products.get(j).getP_height() && product.getP_width() < l_products.get(j).getP_width()) {
                            t_product = l_products.get(j);
                            l_products.set(i, t_product);
                            l_products.set(j, product);
                            product = l_products.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break;
            }
            case 9: {
                int i = 0;
                while (i < l_products.size()) {
                    Product product = l_products.get(i);
                    int j = i + 1;
                    while (j < l_products.size()) {
                        if (product.getP_width() < l_products.get(j).getP_width()) {
                            t_product = l_products.get(j);
                            l_products.set(i, t_product);
                            l_products.set(j, product);
                            product = l_products.get(i);
                        } else if (product.getP_width() == l_products.get(j).getP_width() && product.getP_height() < l_products.get(j).getP_height()) {
                            t_product = l_products.get(j);
                            l_products.set(i, t_product);
                            l_products.set(j, product);
                            product = l_products.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break;
            }
            default: {
                int i = 0;
                while (i < l_products.size()) {
                    Product product = l_products.get(i);
                    int j = i + 1;
                    while (j < l_products.size()) {
                        if (product.getP_width() * 0.1 * (double)score_type + product.getP_height() * (1.0 - 0.1 * (double)score_type) < l_products.get(j).getP_width() * 0.1 * (double)score_type + l_products.get(j).getP_height() * (1.0 - 0.1 * (double)score_type)) {
                            t_product = l_products.get(j);
                            l_products.set(i, t_product);
                            l_products.set(j, product);
                            product = l_products.get(i);
                        }
                        ++j;
                    }
                    ++i;
                }
                break block0;
            }
        }
        return l_products;
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

    public List<Material> scoreYMaterials(List<Material> y_materials) {
        Material t_material = null;
        int i = 0;
        while (i < y_materials.size()) {
            Material material = y_materials.get(i);
            if (material.getM_is_show() == 0) {
                int j = i + 1;
                while (j < y_materials.size()) {
                    if (y_materials.get(j).getM_is_show() == 0 && DecimalMath.sub(material.getR_height(), material.getR_width()) < DecimalMath.sub(y_materials.get(j).getR_height(), y_materials.get(j).getR_width())) {
                        t_material = y_materials.get(j);
                        y_materials.set(i, t_material);
                        y_materials.set(j, material);
                        material = y_materials.get(i);
                    }
                    ++j;
                }
            }
            ++i;
        }
        return y_materials;
    }
}
