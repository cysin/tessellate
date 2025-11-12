/*
 * Decompiled with CFR 0.152.
 */
package com.gv.model;

import java.io.Serializable;
import java.util.List;

public class Product
implements Serializable {
    private static final long serialVersionUID = -7880875675568996833L;
    private String p_no;
    private String p_name;
    private double p_height;
    private double p_width;
    private double p_weight;
    private String p_color;
    private double p_count;
    private int p_is_dir;
    private double m_left;
    private double m_top;
    private double p_n_left;
    private double p_n_top;
    private int p_r_count;
    private int p_is_show;
    private List<Product> p_products;
    private int p_is_copy;
    private int p_is_score;
    private int p_is_dk_score;
    private int p_i_score;
    private int p_p_count;

    public String getP_name() {
        return this.p_name;
    }

    public void setP_name(String p_name) {
        this.p_name = p_name;
    }

    public double getP_height() {
        return this.p_height;
    }

    public void setP_height(double p_height) {
        this.p_height = p_height;
    }

    public double getP_width() {
        return this.p_width;
    }

    public void setP_width(double p_width) {
        this.p_width = p_width;
    }

    public String getP_color() {
        return this.p_color;
    }

    public void setP_color(String p_color) {
        this.p_color = p_color;
    }

    public double getM_left() {
        return this.m_left;
    }

    public void setM_left(double m_left) {
        this.m_left = m_left;
    }

    public double getM_top() {
        return this.m_top;
    }

    public void setM_top(double m_top) {
        this.m_top = m_top;
    }

    public double getP_count() {
        return this.p_count;
    }

    public void setP_count(double p_count) {
        this.p_count = p_count;
    }

    public double getP_n_left() {
        return this.p_n_left;
    }

    public void setP_n_left(double p_n_left) {
        this.p_n_left = p_n_left;
    }

    public double getP_n_top() {
        return this.p_n_top;
    }

    public void setP_n_top(double p_n_top) {
        this.p_n_top = p_n_top;
    }

    public int getP_is_dir() {
        return this.p_is_dir;
    }

    public void setP_is_dir(int p_is_dir) {
        this.p_is_dir = p_is_dir;
    }

    public double getP_weight() {
        return this.p_weight;
    }

    public void setP_weight(double p_weight) {
        this.p_weight = p_weight;
    }

    public int getP_is_show() {
        return this.p_is_show;
    }

    public void setP_is_show(int p_is_show) {
        this.p_is_show = p_is_show;
    }

    public List<Product> getP_products() {
        return this.p_products;
    }

    public void setP_products(List<Product> p_products) {
        this.p_products = p_products;
    }

    public int getP_is_copy() {
        return this.p_is_copy;
    }

    public void setP_is_copy(int p_is_copy) {
        this.p_is_copy = p_is_copy;
    }

    public int getP_r_count() {
        return this.p_r_count;
    }

    public void setP_r_count(int p_r_count) {
        this.p_r_count = p_r_count;
    }

    public String getP_no() {
        return this.p_no;
    }

    public void setP_no(String p_no) {
        this.p_no = p_no;
    }

    public int getP_is_score() {
        return this.p_is_score;
    }

    public void setP_is_score(int p_is_score) {
        this.p_is_score = p_is_score;
    }

    public int getP_is_dk_score() {
        return this.p_is_dk_score;
    }

    public void setP_is_dk_score(int p_is_dk_score) {
        this.p_is_dk_score = p_is_dk_score;
    }

    public int getP_p_count() {
        return this.p_p_count;
    }

    public void setP_p_count(int p_p_count) {
        this.p_p_count = p_p_count;
    }

    public int getP_i_score() {
        return this.p_i_score;
    }

    public void setP_i_score(int p_i_score) {
        this.p_i_score = p_i_score;
    }
}
