/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  com.opensymphony.xwork2.ActionSupport
 */
package com.gv.action;

import com.gv.constant.Constant;
import com.gv.model.Material;
import com.gv.model.Product;
import com.gv.service.ViewServiceR2;
import com.opensymphony.xwork2.ActionSupport;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class ViewAction
extends ActionSupport {
    private static final long serialVersionUID = -7548261859230477083L;
    private String product_no;
    private String product_name;
    private String product_height;
    private String product_width;
    private String product_count;
    private String product_color;
    private String product_weight;
    private String product_is_dir;
    private String material_name;
    private String material_height;
    private String material_width;
    private String material_count;
    private String material_color;
    private String material_weight;
    private double scale;
    private String material_yl;
    private List<Material> materials;
    private double saw_bite;

    public String getProduct_name() {
        return this.product_name;
    }

    public void setProduct_name(String product_name) {
        this.product_name = product_name;
    }

    public String getProduct_height() {
        return this.product_height;
    }

    public void setProduct_height(String product_height) {
        this.product_height = product_height;
    }

    public String getProduct_width() {
        return this.product_width;
    }

    public void setProduct_width(String product_width) {
        this.product_width = product_width;
    }

    public String getProduct_count() {
        return this.product_count;
    }

    public void setProduct_count(String product_count) {
        this.product_count = product_count;
    }

    public List<Material> getMaterials() {
        return this.materials;
    }

    public void setMaterials(List<Material> materials) {
        this.materials = materials;
    }

    public String getMaterial_name() {
        return this.material_name;
    }

    public void setMaterial_name(String material_name) {
        this.material_name = material_name;
    }

    public String getMaterial_height() {
        return this.material_height;
    }

    public void setMaterial_height(String material_height) {
        this.material_height = material_height;
    }

    public String getMaterial_width() {
        return this.material_width;
    }

    public void setMaterial_width(String material_width) {
        this.material_width = material_width;
    }

    public String getMaterial_count() {
        return this.material_count;
    }

    public void setMaterial_count(String material_count) {
        this.material_count = material_count;
    }

    public double getSaw_bite() {
        return this.saw_bite;
    }

    public void setSaw_bite(double saw_bite) {
        this.saw_bite = saw_bite;
    }

    public String getProduct_is_dir() {
        return this.product_is_dir;
    }

    public void setProduct_is_dir(String product_is_dir) {
        this.product_is_dir = product_is_dir;
    }

    public String getProduct_color() {
        return this.product_color;
    }

    public void setProduct_color(String product_color) {
        this.product_color = product_color;
    }

    public String getProduct_weight() {
        return this.product_weight;
    }

    public void setProduct_weight(String product_weight) {
        this.product_weight = product_weight;
    }

    public String getMaterial_color() {
        return this.material_color;
    }

    public void setMaterial_color(String material_color) {
        this.material_color = material_color;
    }

    public String getMaterial_weight() {
        return this.material_weight;
    }

    public void setMaterial_weight(String material_weight) {
        this.material_weight = material_weight;
    }

    public String getMaterial_yl() {
        return this.material_yl;
    }

    public void setMaterial_yl(String material_yl) {
        this.material_yl = material_yl;
    }

    public String getProduct_no() {
        return this.product_no;
    }

    public void setProduct_no(String product_no) {
        this.product_no = product_no;
    }

    public String createView() {
        String[] product_no_arr = this.product_no.split(",");
        String[] product_name_arr = this.product_name.split(",");
        String[] product_height_arr = this.product_height.split(",");
        String[] product_width_arr = this.product_width.split(",");
        String[] product_count_arr = this.product_count.split(",");
        String[] product_is_div_arr = this.product_is_dir.split(",");
        String[] product_weight_arr = this.product_weight.split(",");
        String[] product_color_arr = this.product_color.split(",");
        ArrayList<Product> m_products = new ArrayList<Product>();
        int i = 0;
        while (i < product_name_arr.length) {
            Product product = new Product();
            product.setP_no(product_no_arr[i]);
            product.setP_name(product_name_arr[i]);
            product.setP_height(Double.parseDouble(product_height_arr[i]));
            product.setP_width(Double.parseDouble(product_width_arr[i]));
            product.setP_count(Double.parseDouble(product_count_arr[i]));
            product.setP_color(product_color_arr[i]);
            product.setP_weight(Double.parseDouble(product_weight_arr[i]));
            product.setP_r_count((int)product.getP_count());
            m_products.add(product);
            product = null;
            if (0.0 == Double.parseDouble(product_is_div_arr[i])) {
                product = new Product();
                product.setP_no(product_no_arr[i]);
                product.setP_name(product_name_arr[i]);
                product.setP_width(Double.parseDouble(product_height_arr[i]));
                product.setP_height(Double.parseDouble(product_width_arr[i]));
                product.setP_count(Integer.parseInt(product_count_arr[i]));
                product.setP_color(product_color_arr[i]);
                product.setP_weight(Double.parseDouble(product_weight_arr[i]));
                product.setP_is_copy(1);
                product.setP_r_count((int)product.getP_count());
                m_products.add(product);
                product = null;
            }
            ++i;
        }
        ArrayList<Material> m_materials = new ArrayList<Material>();
        if ("checked".equals(this.material_yl)) {
            String[] material_height_arr = this.material_height.split(",");
            String[] material_width_arr = this.material_width.split(",");
            String[] material_count_arr = this.material_count.split(",");
            String[] material_color_arr = this.material_color.split(",");
            String[] material_weight_arr = this.material_weight.split(",");
            int i2 = 0;
            while (i2 < material_count_arr.length) {
                Material material = new Material();
                material.setM_name(String.valueOf(material_height_arr[i2]) + "x" + material_width_arr[i2]);
                material.setM_height(Double.parseDouble(material_height_arr[i2]));
                material.setM_width(Double.parseDouble(material_width_arr[i2]));
                material.setM_count(Integer.parseInt(material_count_arr[i2]));
                material.setM_weight(Double.parseDouble(material_weight_arr[i2]));
                material.setM_color(material_color_arr[i2]);
                material.setR_height(Double.parseDouble(material_height_arr[i2]) - 6.0);
                material.setR_width(Double.parseDouble(material_width_arr[i2]) - 6.0);
                material.setM_is_yl(1);
                m_materials.add(material);
                material = null;
                ++i2;
            }
        }
        Set<String> m_set = this.processProducts();
        for (String key : m_set) {
            Material material = new Material();
            material.setM_name(String.valueOf(this.material_name) + " \u544e");
            material.setM_height(Constant.getMaterialC().get(this.material_name).getM_height());
            material.setM_width(Constant.getMaterialC().get(this.material_name).getM_width());
            material.setM_count(1000000.0);
            material.setM_weight(Double.parseDouble(key.split(":")[0]));
            material.setM_color(key.split(":")[1]);
            material.setR_height(Constant.getMaterialC().get(this.material_name).getM_height() - 6.0);
            material.setR_width(Constant.getMaterialC().get(this.material_name).getM_width() - 6.0);
            m_materials.add(material);
            material = null;
        }
        ViewServiceR2 vs = new ViewServiceR2();
        this.materials = vs.createView(m_products, m_materials, this.saw_bite, this.scale);
        return "success";
    }

    private Set<String> processProducts() {
        HashSet<String> p_set = new HashSet<String>();
        String[] product_weight_arr = this.product_weight.split(",");
        String[] product_color_arr = this.product_color.split(",");
        int i = 0;
        while (i < product_weight_arr.length) {
            p_set.add(String.valueOf(product_weight_arr[i]) + ":" + product_color_arr[i]);
            ++i;
        }
        return p_set;
    }

    public double getScale() {
        return this.scale;
    }

    public void setScale(double scale) {
        this.scale = scale;
    }
}
