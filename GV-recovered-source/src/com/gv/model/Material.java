/*
 * Decompiled with CFR 0.152.
 */
package com.gv.model;

import com.gv.model.Product;
import java.io.Serializable;
import java.util.List;
import java.util.Map;

public class Material
implements Serializable {
    private static final long serialVersionUID = 155674622680398141L;
    private String m_name;
    private double m_height;
    private double m_width;
    private String m_color;
    private double m_weight;
    private double r_height;
    private double r_width;
    private double m_count;
    private int m_u_count = 1;
    private Map<Double, Double> m_l_scale;
    private Map<Double, Double> m_t_scale;
    private int m_is_show;
    private List<Product> m_products;
    private List<Material> m_materials;
    private Map<String, List<Material>> m_material_map;
    private int m_f_id;
    private int m_node_id;
    private int m_c_type;
    private int m_hs_type;
    private double m_area_used;
    private double m_m_left;
    private double m_m_top;
    private int m_is_used;
    private int m_is_yj;
    private int m_y_is_ud;
    private List<Material> m_y_materials;
    private List<Product> m_i_products;
    private int m_is_yl;
    private int m_is_dk;
    private int m_is_p_info;
    private int m_f_c_type;
    private int m_f_f_id;

    public String getM_name() {
        return this.m_name;
    }

    public void setM_name(String m_name) {
        this.m_name = m_name;
    }

    public double getM_height() {
        return this.m_height;
    }

    public void setM_height(double m_height) {
        this.m_height = m_height;
    }

    public double getM_width() {
        return this.m_width;
    }

    public void setM_width(double m_width) {
        this.m_width = m_width;
    }

    public String getM_color() {
        return this.m_color;
    }

    public void setM_color(String m_color) {
        this.m_color = m_color;
    }

    public List<Product> getM_products() {
        return this.m_products;
    }

    public void setM_products(List<Product> m_products) {
        this.m_products = m_products;
    }

    public double getM_count() {
        return this.m_count;
    }

    public void setM_count(double m_count) {
        this.m_count = m_count;
    }

    public double getR_height() {
        return this.r_height;
    }

    public void setR_height(double r_height) {
        this.r_height = r_height;
    }

    public double getR_width() {
        return this.r_width;
    }

    public void setR_width(double r_width) {
        this.r_width = r_width;
    }

    public int getM_u_count() {
        return this.m_u_count;
    }

    public void setM_u_count(int m_u_count) {
        this.m_u_count = m_u_count;
    }

    public Map<Double, Double> getM_l_scale() {
        return this.m_l_scale;
    }

    public void setM_l_scale(Map<Double, Double> m_l_scale) {
        this.m_l_scale = m_l_scale;
    }

    public Map<Double, Double> getM_t_scale() {
        return this.m_t_scale;
    }

    public void setM_t_scale(Map<Double, Double> m_t_scale) {
        this.m_t_scale = m_t_scale;
    }

    public int getM_is_show() {
        return this.m_is_show;
    }

    public void setM_is_show(int m_is_show) {
        this.m_is_show = m_is_show;
    }

    public double getM_weight() {
        return this.m_weight;
    }

    public void setM_weight(double m_weight) {
        this.m_weight = m_weight;
    }

    public List<Material> getM_materials() {
        return this.m_materials;
    }

    public void setM_materials(List<Material> m_materials) {
        this.m_materials = m_materials;
    }

    public Map<String, List<Material>> getM_material_map() {
        return this.m_material_map;
    }

    public void setM_material_map(Map<String, List<Material>> m_material_map) {
        this.m_material_map = m_material_map;
    }

    public int getM_f_id() {
        return this.m_f_id;
    }

    public void setM_f_id(int m_f_id) {
        this.m_f_id = m_f_id;
    }

    public int getM_node_id() {
        return this.m_node_id;
    }

    public void setM_node_id(int m_node_id) {
        this.m_node_id = m_node_id;
    }

    public int getM_c_type() {
        return this.m_c_type;
    }

    public void setM_c_type(int m_c_type) {
        this.m_c_type = m_c_type;
    }

    public double getM_area_used() {
        return this.m_area_used;
    }

    public void setM_area_used(double m_area_used) {
        this.m_area_used = m_area_used;
    }

    public int getM_hs_type() {
        return this.m_hs_type;
    }

    public void setM_hs_type(int m_hs_type) {
        this.m_hs_type = m_hs_type;
    }

    public double getM_m_left() {
        return this.m_m_left;
    }

    public void setM_m_left(double m_m_left) {
        this.m_m_left = m_m_left;
    }

    public double getM_m_top() {
        return this.m_m_top;
    }

    public void setM_m_top(double m_m_top) {
        this.m_m_top = m_m_top;
    }

    public int getM_is_used() {
        return this.m_is_used;
    }

    public void setM_is_used(int m_is_used) {
        this.m_is_used = m_is_used;
    }

    public List<Material> getM_y_materials() {
        return this.m_y_materials;
    }

    public void setM_y_materials(List<Material> m_y_materials) {
        this.m_y_materials = m_y_materials;
    }

    public int getM_is_yj() {
        return this.m_is_yj;
    }

    public void setM_is_yj(int m_is_yj) {
        this.m_is_yj = m_is_yj;
    }

    public int getM_y_is_ud() {
        return this.m_y_is_ud;
    }

    public void setM_y_is_ud(int m_y_is_ud) {
        this.m_y_is_ud = m_y_is_ud;
    }

    public List<Product> getM_i_products() {
        return this.m_i_products;
    }

    public void setM_i_products(List<Product> m_i_products) {
        this.m_i_products = m_i_products;
    }

    public int getM_is_yl() {
        return this.m_is_yl;
    }

    public void setM_is_yl(int m_is_yl) {
        this.m_is_yl = m_is_yl;
    }

    public int getM_is_dk() {
        return this.m_is_dk;
    }

    public void setM_is_dk(int m_is_dk) {
        this.m_is_dk = m_is_dk;
    }

    public int getM_is_p_info() {
        return this.m_is_p_info;
    }

    public void setM_is_p_info(int m_is_p_info) {
        this.m_is_p_info = m_is_p_info;
    }

    public int getM_f_c_type() {
        return this.m_f_c_type;
    }

    public void setM_f_c_type(int m_f_c_type) {
        this.m_f_c_type = m_f_c_type;
    }

    public int getM_f_f_id() {
        return this.m_f_f_id;
    }

    public void setM_f_f_id(int m_f_f_id) {
        this.m_f_f_id = m_f_f_id;
    }
}
