<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>开板</title>
<link rel="stylesheet" href="css/style.css" type="text/css" />
<script type="text/javascript" src="js/jquery-1.7.2.js"></script>
<script type="text/javascript">
	$("document")
			.ready(
					function() {

						$(window).scroll(function() {
							var top = $(window).scrollTop() + 600;
							$("#returninfo").css({
								marginTop : top + "px"
							});
							$("#print").css({
								marginTop : top + "px"
							});
						});

						$("#t_y_table").hide();
						$("#tt_y_table").hide();
						$("#d_y_table").hide();
						$("#b_y_table").hide();
						$("#bc_table").hide();
						$("#bb_table").hide();

						$("#loading").hide();

						$("#addbut")
								.click(
										function() {
											var product_nos = $("input[id='product_nos']");
											var product_names = $("input[id='product_names']");
											var product_heights = $("input[id='product_heights']");
											var product_widths = $("input[id='product_widths']");
											var product_counts = $("input[id='product_counts']");
											var product_colors = $("input[id='product_colors']");
											var product_weights = $("input[id='product_weights']");
											//余料
											var material_heights = $("input[id='material_heights']");
											var material_widths = $("input[id='material_widths']");
											var material_counts = $("input[id='material_counts']");
											var material_colors = $("input[id='material_colors']");
											var material_weights = $("input[id='material_weights']");

											//板材
											//var material_names = $("select[id='material_names']");

											var product_no = "";
											var product_name = "";
											var product_height = "";
											var product_width = "";
											var product_count = "";
											var product_is_dir = "";
											var product_weight = "";
											var product_color = "";

											//余料
											var material_height = "";
											var material_width = "";
											var material_count = "";
											var material_color = "";
											var material_weight = "";
											//板材
											//var material_name = $("select[id='material_names']");

											var product_is_dirs = $("select[id='is_direction']");
											var url = "createView.action";
											//alert("sss");
											var c = /^\d{1,}$/;
											if ('checked' == $("#kc").attr(
													"checked")) {
												for ( var i = 0; i < material_heights.length; i++) {
													if (!c
															.exec($(
																	material_heights[i])
																	.val())) {
														alert("余料长度只能输入数字");
														return false;
													}
													if (!c.exec($(
															material_widths[i])
															.val())) {
														alert("余料宽度只能输入数字");
														return false;
													}
													if (!c.exec($(
															material_counts[i])
															.val())) {
														alert("余料数量只能输入数字");
														return false;
													}
													if (!c
															.exec($(
																	material_weights[i])
																	.val())) {
														alert("余料厚度只能输入数字");
														return false;
													}

													if ("" == $(
															material_colors[i])
															.val()) {
														alert("余料花色不能为空");
														return false;
													}
												}

												for ( var i = 0; i < material_heights.length; i++) {
													material_height = material_height
															+ material_heights[i].value
															+ ",";
													material_width = material_width
															+ material_widths[i].value
															+ ",";
													material_count = material_count
															+ material_counts[i].value
															+ ",";
													material_color = material_color
															+ material_colors[i].value
															+ ",";
													material_weight = material_weight
															+ material_weights[i].value
															+ ",";
												}
											}

											//alert("sss");
											for ( var i = 0; i < product_names.length; i++) {
												product_no = product_no
														+ product_nos[i].value
														+ ",";
												product_name = product_name
														+ product_names[i].value
														+ ",";
												product_height = product_height
														+ product_heights[i].value
														+ ",";
												product_width = product_width
														+ product_widths[i].value
														+ ",";
												product_count = product_count
														+ product_counts[i].value
														+ ",";
												product_is_dir = product_is_dir
														+ product_is_dirs[i].value
														+ ",";
												product_weight = product_weight
														+ product_weights[i].value
														+ ",";
												product_color = product_color
														+ product_colors[i].value
														+ ",";
											}
											//alert("sss");

											var scale = parseFloat($("#scale")
													.val());

											//alert(scale);

											if (0 >= scale || 1 <= scale) {
												alert("只能为0-1之间的数");
												return false;
											}

											//alert("sss");
											var params = {
												product_no : product_no,
												product_name : product_name,
												product_height : product_height,
												product_width : product_width,
												product_count : product_count,
												product_weight : product_weight,
												product_color : product_color,
												material_name : $(
														"#material_name").val(),
												material_height : material_height,
												material_width : material_width,
												material_count : material_count,
												material_weight : material_weight,
												material_color : material_color,
												material_yl : $("#kc").attr(
														"checked"),
												saw_bite : $("#saw_bite").val(),
												product_is_dir : product_is_dir,
												scale : $("#scale").val()
											};
											$("#iTable").hide();
											$("#loading").show();

											$.post(url, params, callback,
													'json');
										});

						$("#addrow")
								.click(
										function() {
											var _len = $("#table tr").length;
											//alert(_len);

											//alert($("#tr" + (_len - 1)).html());

											var addStr = $(
													"tr[name='tr" + _len + "']")
													.html();

											//alert(addStr);

											if (1 == _len) {
												addStr = addStr
														.replace(
																"&nbsp;",
																"<img src='sc.jpg' onclick=\"delrow("
																		+ (_len + 1)
																		+ ")\" width='20' />");

											} else {
												addStr = addStr.replace(
														"delrow(" + _len + ")",
														"delrow(" + (_len + 1)
																+ ")");
											}

											addStr = addStr.replace("p_index"
													+ _len + "", "p_index"
													+ (_len + 1) + "");

											addStr = addStr.replace("t_img"
													+ _len + "", "t_img"
													+ (_len + 1) + "");	
											
											addStr = addStr.replace("dir"
													+ _len + "", "dir"
													+ (_len + 1) + "");											

											addStr = addStr.replace("img_"
													+ _len + "", "img_"
													+ (_len + 1) + "");

											addStr = addStr.replace(
													"changeImg(this," + _len
															+ ")",
													"changeImg(this,"
															+ (_len + 1) + ")");

											//alert(addStr);
											var tr = "";
											if (1 == _len % 2) {
												tr = "<tr id=tr"
														+ (_len + 1)
														+ " name=tr"
														+ (_len + 1)
														+ " bgcolor='#d8d9db' >"
														+ addStr + "</tr>";
											} else {
												tr = "<tr id=tr"
														+ (_len + 1)
														+ " name=tr"
														+ (_len + 1)
														+ " bgcolor='#ffffff' >"
														+ addStr + "</tr>";
											}
											//alert(tr);

											$("#table").append(tr);

											$("#p_index" + (_len + 1)).text(
													(_len + 1));
										});

						$("#addrowm")
								.click(
										function() {
											var _len = $("#tablem tr").length;
											//alert(_len);

											//alert($("#tr" + (_len - 1)).html());

											var addStr = $(
													"tr[name='trm" + _len
															+ "']").html();

											if (1 == _len) {
												addStr = addStr
														.replace(
																"&nbsp;",
																"<img src='sc.jpg' onclick=\"delrowm("
																		+ (_len + 1)
																		+ ")\" width='20' />");

											} else {
												addStr = addStr
														.replace(
																"delrowm("
																		+ _len
																		+ ")",
																"delrowm("
																		+ (_len + 1)
																		+ ")");
											}
											//alert(addStr);
											var tr = "";
											if (1 == _len % 2) {
												tr = "<tr id=trm"
														+ (_len + 1)
														+ " name=trm"
														+ (_len + 1)
														+ " bgcolor='#d8d9db' >"
														+ addStr + "</tr>";
											} else {
												tr = "<tr id=trm"
														+ (_len + 1)
														+ " name=trm"
														+ (_len + 1)
														+ " bgcolor='#ffffff' >"
														+ addStr + "</tr>";
											}
											//alert(tr);
											$("#tablem").append(tr);
										});
						$("#pro_com")
								.click(
										function() {
											var product_nos = $("input[id='product_nos']");
											var product_names = $("input[id='product_names']");
											var product_heights = $("input[id='product_heights']");
											var product_widths = $("input[id='product_widths']");
											var product_counts = $("input[id='product_counts']");
											var product_colors = $("input[id='product_colors']");
											var product_weights = $("input[id='product_weights']");

											var c = /^\d{1,}$/;

											for ( var i = 0; i < product_names.length; i++) {
												if ("" == $(product_nos[i])
														.val()) {
													alert("产品编码不能为空");
													return false;
												}

												if ("" == $(product_names[i])
														.val()) {
													alert("产品名称不能为空");
													return false;
												}

												if (!c.exec($(
														product_heights[i])
														.val())) {
													alert("产品长度只能输入数字");
													return false;
												}
												if (!c
														.exec($(
																product_widths[i])
																.val())) {
													alert("产品宽度只能输入数字");
													return false;
												}
												if (!c
														.exec($(
																product_counts[i])
																.val())) {
													alert("产品数量只能输入数字");
													return false;
												}
												if (!c.exec($(
														product_weights[i])
														.val())) {
													alert("产品厚度只能输入数字");
													return false;
												}

												if ("" == $(product_colors[i])
														.val()) {
													alert("产品花色不能为空");
													return false;
												}
											}

											//产品重名验证
											for ( var i = 0; i < product_names.length; i++) {

												for ( var j = i + 1; j < product_nos.length; j++) {
													if (product_nos[i].value == product_nos[j].value) {
														 
															alert("存在相同编码的产品,产品编码唯一！");
															return false;
														
													}
												}
											}

											$("#d_table").hide();
											$("#t_table").hide();
											$("#tt_table").hide();
											$("#b_table").hide();
											//$("#table_but").hide();
											$("#t_y_table").show();
											$("#bc_table").show();
											$("#bb_table").show();
											if ('checked' == $("#kc").attr(
													"checked")) {
												$("#tt_y_table").show();
												$("#d_y_table").show();
												$("#b_y_table").show();
											} else {
												$("#tt_y_table").hide();
												$("#d_y_table").hide();
												$("#b_y_table").hide();
											}
										});
						$("#kc").click(function() {
							if ('checked' == $("#kc").attr("checked")) {
								$("#tt_y_table").show();
								$("#d_y_table").show();
								$("#b_y_table").show();
							} else {
								$("#tt_y_table").hide();
								$("#d_y_table").hide();
								$("#b_y_table").hide();
							}
						});

						$("#addr").click(function() {
							//alert("sdfsdfsdf");
							$("#table").show();
							$("#table_but").show();
							$("#tablem_kc").hide();
							$("#tablem_bc").hide();
						});

					});
	function delrow(rowid) {
		$("tr[name='tr" + rowid + "']").remove();
		//alert(rowid);
		var _l = $("#table tr").length;
		//alert(_l);
		for ( var i = rowid + 1; i <= _l + 1; i++) {
			$("tr[name=tr" + i + "]").attr("name", "tr" + (i - 1));

			var hText = $("tr[name=tr" + (i - 1) + "]").html();

			//alert(hText);

			hText = hText.replace("delrow(" + i + ")", "delrow(" + (i - 1)
					+ ")");

			hText = hText.replace("p_index" + i + "", "p_index" + (i - 1)
					+ "");

			hText = hText.replace("t_img" + i + "", "t_img" + (i - 1)
					+ "");
			
			hText = hText.replace("dir" + i + "", "dir" + (i - 1)
					+ "");
			
			hText = hText.replace("img_" + i + "", "img_" + (i - 1) + "");

			hText = hText.replace("changeImg(this," + i + ")",
					"changeImg(this," + (i - 1) + ")");

			//alert(hText);

			$("tr[name=tr" + (i - 1) + "]").html(hText);

			$("#p_index" + (i - 1)).text((i - 1));

			if (0 == (i - 1) % 2) {
				$("tr[name=tr" + (i - 1) + "]").css({
					"background-color" : "#d8d9db"
				});
			} else {
				$("tr[name=tr" + (i - 1) + "]").css({
					"background-color" : "#ffffff"
				});
			}

			
		}
		//alert($("#iTable").html());
	}

	function delrowm(rowid) {

		$("tr[name='trm" + rowid + "']").remove();
		//alert(rowid);
		var _l = $("#tablem tr").length;
		for ( var i = rowid + 1; i <= _l + 1; i++) {
			$("tr[name=trm" + i + "]").attr("name", "trm" + (i - 1));

			var hText = $("tr[name=trm" + (i - 1) + "]").html();

			//alert(hText);

			hText = hText.replace("delrowm(" + i + ")", "delrowm(" + (i - 1)
					+ ")");

			//alert(hText);

			$("tr[name=trm" + (i - 1) + "]").html(hText);

			if (0 == (i - 1) % 2) {
				$("tr[name=trm" + (i - 1) + "]").css({
					"background-color" : "#d8d9db"
				});
			} else {
				$("tr[name=trm" + (i - 1) + "]").css({
					"background-color" : "#ffffff"
				});
			}
		}
	}

	function callback(data) {
		var saw_bite = $("#saw_bite").val();
		//alert(saw_bite);
		$("#panel").html("");
		$("#loading").hide();
		var htmlText = "";

		htmlText = htmlText
				+ "<img src='fh.jpg' width='120' style='position: absolute;margin-left:1150px;margin-top:600px;' id='returninfo' onclick='returnInfo()' />";

		htmlText = htmlText
				+ "<img src='dy.jpg' width='120' style='position: absolute;margin-left:1280px;margin-top:600px;' id='print' onclick='printInfo()' />";
		var p_no = 0;
		//alert(data.length);
		for ( var i = 0; i < data.length; i++) {

			//alert(i);
			/*htmlText = htmlText
					+ "<div style='width:756px;height:1086px;border:1px solid #000000;'><div style='text-align:center;'>原料名称："
					+ data[i].m_name + "</div><br />";*/
			/*htmlText = htmlText
					+ "<div style='width:756px;height:1086px;border:1px solid #000000;'>";
			if (data[i].m_width > 1086) {
				data[i].m_width = 1086;
			}
			if (data[i].m_height > 756) {
				data[i].m_height = 756;
			}*/
			//var height = document.documentElement.clientHeight;
			//var width = document.documentElement.clientWidth;
			if (i < data.length - 1) {
				if (0 == data[i].m_is_show) {
					p_no = p_no + 1;
					htmlText = htmlText
							+ "<div class='b_div' style='position: absolute;margin-top:"
							+ ((p_no - 1) * 749)
							+ "px;width: 1078px;height:749px;background-color:#fff;'>";

					//alert(htmlText);

					//颜色、厚度、花色等
					htmlText = htmlText
							+ "<div style='font-size:11px;font-family:黑体;position: absolute;width: 130px;height:20px;margin-left:615px;margin-top:700px;text-align:left;border-left:1px solid;border-top:1px solid;border-right:1px solid;line-height:20px;border-bottom:1px solid #d1d2d4;'>&nbsp;&nbsp;板材厚度:&nbsp;"
							+ data[i].m_weight + "&nbsp;mm</div>";
					htmlText = htmlText
							+ "<div style='font-size:11px;font-family:黑体;position: absolute;width: 120px;height:20px;margin-left:745px;margin-top:700px;text-align:left;border-top:1px solid;border-right:1px solid;line-height:20px;border-bottom:1px solid #d1d2d4;'>&nbsp;&nbsp;板材规格:&nbsp;"
							+ data[i].m_name + "</div>";

					htmlText = htmlText
							+ "<div style='font-size:11px;font-family:黑体;position: absolute;width: 130px;height:20px;margin-left:615px;margin-top:721px;text-align:left;border-left:1px solid;border-bottom:1px solid;border-right:1px solid;line-height:20px;'>&nbsp;&nbsp;饰面花色:&nbsp;"
							+ data[i].m_color + "</div>";
					htmlText = htmlText
							+ "<div style='font-size:11px;font-family:黑体;position: absolute;width: 120px;height:20px;margin-left:745px;margin-top:721px;text-align:left;border-bottom:1px solid;border-right:1px solid;line-height:20px;'>&nbsp;&nbsp;开板数量:&nbsp;"
							+ data[i].m_u_count + "&nbsp;张</div>";
					/* htmlText = htmlText
							+ "<div style='font-size:16px;font-family:黑体;position: absolute;width: 200px;height:60px;margin-left:880px;margin-top:70px;text-align:left;'>易道魔方系统</div>"; */
					//底部Logo
					htmlText = htmlText
							+ "<img src='LOGO.png' style='position: absolute;margin-top:685px;margin-left:900px;' width='100'/>";

					//页码
					htmlText = htmlText
							+ "<div style='font-size:11px;font-family:黑体;position: absolute;width: 250px;height:30px;margin-left:743px;margin-top:50px;text-align:right;'>本次开板图纸：&nbsp;共&nbsp;pagecount&nbsp;页&nbsp;/&nbsp;第&nbsp;"
							+ p_no + "&nbsp;页</div>";

					//产品信息
					htmlText = htmlText
							+ "<div style='font-size:11px;font-family:黑体;position: absolute;width: 900px;height:25px;margin-left:80px;margin-top:550px;'>";

					//var p_count = data[i].m_i_products.length / 6;
					var p_count = 1;
					for ( var p = 0; p <= p_count; p++) {
						var f_p = p;
						htmlText = htmlText
								+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;line-height:18px;width:40px;margin-top:0px;text-align:left;margin-left:"
								+ (f_p * 470 + 70) + "px;'>代码</div>";
						htmlText = htmlText
								+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;line-height:18px;width:40px;margin-top:0px;text-align:left;margin-left:"
								+ (f_p * 470 + 175) + "px;'>名称</div>";
						htmlText = htmlText
								+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;line-height:18px;width:40px;margin-top:0px;text-align:left;margin-left:"
								+ (f_p * 470 + 290) + "px;'>规格</div>";
						htmlText = htmlText
								+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;line-height:18px;width:80px;margin-top:0px;text-align:left;margin-left:"
								+ (f_p * 470 + 380) + "px;'>数量/统计</div>";
						/* for ( var j = p * 6; j < data[i].m_i_products.length; j++) { */

						for ( var j = p * 6; j < ((p + 1) * 6); j++) {

							if (5 == j % 6) {
								if (j < data[i].m_i_products.length) {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;width:450px;line-height:18px;border-left:1px solid;border-right:1px solid;border-bottom:1px solid;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:120px;'>&nbsp;"
											+ data[i].m_i_products[j].p_no
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:132px;width:130px;'>&nbsp;"
											+ data[i].m_i_products[j].p_name
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:260px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_height
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:285px;width:7px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:292px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_width
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:317px;width:8px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:325px;width:10px;text-align:left;'>"
											+ data[i].m_weight + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:345px;width:15px;text-align:right;'>&nbsp;"
											+ data[i].m_i_products[j].p_count
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:360px;width:20px;'>块x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:375px;width:20px;text-align:right;'>"
											+ data[i].m_u_count + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:395px;width:20px;'>张=</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:413px;width:22px;text-align:left;'>"
											+ (data[i].m_i_products[j].p_count * data[i].m_u_count)
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:435px;width:18px;text-align:left;'>块</div>";

									htmlText = htmlText + "</div>";
								} else {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;width:450px;line-height:18px;border-left:1px solid;border-right:1px solid;border-bottom:1px solid;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:420px;'>&nbsp;</div></div>";

								}

							} else if (0 == j % 6) {
								if (j < data[i].m_i_products.length) {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;background-color:#e1e2e4;font-family:黑体;height:18px;width:450px;line-height:18px;border-top:1px solid;border-left:1px solid;border-right:1px solid;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:120px;'>&nbsp;"
											+ data[i].m_i_products[j].p_no
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:132px;width:130px;'>&nbsp;"
											+ data[i].m_i_products[j].p_name
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:260px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_height
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:285px;width:7px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:292px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_width
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:317px;width:8px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:325px;width:10px;text-align:left;'>"
											+ data[i].m_weight + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:345px;width:15px;text-align:right;'>&nbsp;"
											+ data[i].m_i_products[j].p_count
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:360px;width:20px;'>块x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:375px;width:20px;text-align:right;'>"
											+ data[i].m_u_count + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:395px;width:20px;'>张=</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:413px;width:22px;text-align:left;'>"
											+ (data[i].m_i_products[j].p_count * data[i].m_u_count)
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:435px;width:18px;text-align:left;'>块</div>";

									htmlText = htmlText + "</div>";
								} else {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;background-color:#e1e2e4;font-family:黑体;height:18px;width:450px;line-height:18px;border-top:1px solid;border-left:1px solid;border-right:1px solid;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:420px;'>&nbsp;</div></div>";

								}

							}

							else if (0 == j % 2) {
								if (j < data[i].m_i_products.length) {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;background-color:#e1e2e4;font-family:黑体;height:18px;border-left:1px solid;border-right:1px solid;width:450px;line-height:18px;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:120px;'>&nbsp;"
											+ data[i].m_i_products[j].p_no
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:132px;width:130px;'>&nbsp;"
											+ data[i].m_i_products[j].p_name
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:260px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_height
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:285px;width:7px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:292px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_width
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:317px;width:8px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:325px;width:10px;text-align:left;'>"
											+ data[i].m_weight + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:345px;width:15px;text-align:right;'>&nbsp;"
											+ data[i].m_i_products[j].p_count
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:360px;width:20px;'>块x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:375px;width:20px;text-align:right;'>"
											+ data[i].m_u_count + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:395px;width:20px;'>张=</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:413px;width:22px;text-align:left;'>"
											+ (data[i].m_i_products[j].p_count * data[i].m_u_count)
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:435px;width:18px;text-align:left;'>块</div>";

									htmlText = htmlText + "</div>";
								} else {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;background-color:#e1e2e4;font-family:黑体;height:18px;border-left:1px solid;border-right:1px solid;width:450px;line-height:18px;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:420px;'>&nbsp;</div></div>";
								}

							} else {
								if (j < data[i].m_i_products.length) {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;border-left:1px solid;border-right:1px solid;width:450px;line-height:18px;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:120px;'>&nbsp;"
											+ data[i].m_i_products[j].p_no
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:132px;width:130px;'>&nbsp;"
											+ data[i].m_i_products[j].p_name
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:260px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_height
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:285px;width:7px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:292px;width:25px;text-align:left;'>"
											+ data[i].m_i_products[j].p_width
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:317px;width:8px;text-align:left;'>x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:325px;width:10px;text-align:left;'>"
											+ data[i].m_weight + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:345px;width:15px;text-align:right;'>&nbsp;"
											+ data[i].m_i_products[j].p_count
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:360px;width:20px;'>块x</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:375px;width:20px;text-align:right;'>"
											+ data[i].m_u_count + "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:395px;width:20px;'>张=</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:413px;width:22px;text-align:left;'>"
											+ (data[i].m_i_products[j].p_count * data[i].m_u_count)
											+ "</div>";
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:435px;width:18px;text-align:left;'>块</div>";

									htmlText = htmlText + "</div>";
									//alert("sdfsdf");
								} else {
									htmlText = htmlText
											+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:18px;width:450px;line-height:18px;border-left:1px solid;border-right:1px solid;text-align:left;margin-top: "
											+ ((j - p * 6) * 18 + 18)
											+ "px;margin-left: " + (473 * f_p)
											+ "px;'>";

									if (j < 9) {

										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;0"
												+ (j + 1) + "</div>";
									} else {
										htmlText = htmlText
												+ "<div style='position: absolute;border-right:1px solid;width:15px;'>&nbsp;"
												+ (j + 1) + "</div>";
									}
									htmlText = htmlText
											+ "<div style='position: absolute;margin-left:20px;width:420px;'>&nbsp;</div></div>";
								}
							}
						}
					}
					htmlText = htmlText + "</div>";

					//余料信息
					htmlText = htmlText
							+ "<div style='position: absolute;font-size:12px;font-family:黑体;margin-top:700px;height :40px;margin-left:80px;line-height:19px;width:48px;text-align:center;border:1px solid;'>回库<br />余料</div> ";
					var y_l = data[i].m_y_materials.length;
					if (6 < y_l) {
						y_l = 6;
					}
					var y_f = 0;
					for ( var j = 0; j < y_l; j++) {

						if (60 <= (parseInt(data[i].m_y_materials[j].r_width))
								&& 60 <= (parseInt(data[i].m_y_materials[j].r_height))) {

							var m = parseInt(y_f % 2);
							var ll = parseInt(y_f / 2);
							if (0 == m) {
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;background-color:#e1e2e4;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 130)
										+ "px; margin-top:700px;width:20px;text-align:center;border-top:1px solid;'>"
										+ (y_f + 1) + "</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 150)
										+ "px; margin-top:700px;width:32px;text-align:right;border-top:1px solid;border-left:1px solid;'>"
										+ parseInt(data[i].m_y_materials[j].r_height)
										+ "&nbsp;</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 182)
										+ "px; margin-top:700px;width:8px;text-align:right;border-top:1px solid;'>x</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 190)
										+ "px; margin-top:700px;width:25px;text-align:right;border-top:1px solid;'>"
										+ parseInt(data[i].m_y_materials[j].r_width)
										+ "</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 215)
										+ "px; margin-top:700px;width:10px;text-align:right;border-top:1px solid;'>x</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 225)
										+ "px; margin-top:700px;width:12px;text-align:right;border-top:1px solid;'>"
										+ data[i].m_weight + "</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 235)
										+ "px; margin-top:700px;width:49px;text-align:right;border-top:1px solid;border-right:1px solid;'>=&nbsp;"
										+ data[i].m_u_count
										+ "&nbsp;块&nbsp;&nbsp;&nbsp;</div>";
							} else {
								//alert(ll);
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;background-color:#e1e2e4;height:20px;line-height:19px;margin-left:"
										+ (ll * 155 + 130)
										+ "px;text-align:center; margin-top:"
										+ (700 + m * 20)
										+ "px;width:20px;border-bottom:1px solid;border-top:1px solid;border-top:1px solid;'>"
										+ (y_f + 1) + "</div>";

								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 150)
										+ "px;  margin-top:"
										+ (700 + m * 20)
										+ "px;width:32px;text-align:right;border-bottom:1px solid;border-left:1px solid;border-top:1px solid;'>"
										+ parseInt(data[i].m_y_materials[j].r_height)
										+ "&nbsp;</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 182)
										+ "px;  margin-top:"
										+ (700 + m * 20)
										+ "px;width:8px;text-align:right;border-bottom:1px solid;border-top:1px solid;'>x</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 190)
										+ "px;  margin-top:"
										+ (700 + m * 20)
										+ "px;width:25px;text-align:right;border-bottom:1px solid;border-top:1px solid;'>"
										+ parseInt(data[i].m_y_materials[j].r_width)
										+ "</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 215)
										+ "px;  margin-top:"
										+ (700 + m * 20)
										+ "px;width:10px;text-align:right;border-bottom:1px solid;border-top:1px solid;'>x</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 225)
										+ "px;  margin-top:"
										+ (700 + m * 20)
										+ "px;width:12px;text-align:right;border-bottom:1px solid;border-top:1px solid;'>"
										+ data[i].m_weight + "</div>";
								htmlText = htmlText
										+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
										+ (ll * 155 + 235)
										+ "px;  margin-top:"
										+ (700 + m * 20)
										+ "px;width:49px;text-align:right;border-bottom:1px solid;border-right:1px solid;border-top:1px solid;'>=&nbsp;"
										+ data[i].m_u_count
										+ "&nbsp;块&nbsp;&nbsp;&nbsp;</div>";

							}
							y_f = y_f + 1;

						}
					}

					for ( var j = y_f; j < 6; j++) {

						var m = parseInt(y_f % 2);
						var ll = parseInt(y_f / 2);
						if (0 == m) {
							htmlText = htmlText
									+ "<div style='position: absolute;font-size:11px;font-family:黑体;background-color:#e1e2e4;height:20px;line-height:20px;margin-left:"
									+ (ll * 155 + 130)
									+ "px; margin-top:700px;width:20px;text-align:center;border-top:1px solid;'>"
									+ (y_f + 1) + "</div>";
							htmlText = htmlText
									+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
									+ (ll * 155 + 150)
									+ "px; margin-top:700px;width:133px;text-align:right;border-top:1px solid;border-right:1px solid;border-left:1px solid;'>&nbsp;</div>";
						} else {
							//alert(ll);
							htmlText = htmlText
									+ "<div style='position: absolute;font-size:11px;font-family:黑体;background-color:#e1e2e4;height:20px;line-height:19px;margin-left:"
									+ (ll * 155 + 130)
									+ "px; margin-top:"
									+ (700 + m * 20)
									+ "px;width:20px;text-align:center;border-bottom:1px solid ;border-top:1px solid;'>"
									+ (y_f + 1) + "</div>";

							htmlText = htmlText
									+ "<div style='position: absolute;font-size:11px;font-family:黑体;height:20px;line-height:20px;margin-left:"
									+ (ll * 155 + 150)
									+ "px;  margin-top:"
									+ (700 + m * 20)
									+ "px;width:133px;text-align:right;border-bottom:1px solid;border-right:1px solid;border-left:1px solid;border-top:1px solid;'>&nbsp;</div>";

						}
						y_f = y_f + 1;

					}

					//开板图
					var h_scale = 0.37;
					var w_scale = 0.37;
					htmlText = htmlText
							+ "<div class='m_div' style='background-color:#ffffff;position: absolute;height: "
							+ ((data[i].m_width) * w_scale)
							+ "px;width:"
							+ ((data[i].m_height) * h_scale)
							+ "px;margin-left:90px;margin-top:70px;border:2px solid;'>";
					//alert(data[i].m_products.length);
					//alert(data[i].m_products.length);
					//alert(data[i].r_width);
					//alert(data[i].r_height);
					//alert(w_scale);
					//alert(data[0].m_products.length);
					for ( var j = 0; j < data[i].m_products.length; j++) {
						//alert(j);
						//alert(data[i].m_products[j].p_width * w_scale);
						//alert(data[i].m_products[j].p_width * w_scale);
						//alert((parseInt(data[i].m_products[j].p_width) + parseInt(saw_bite)));
						htmlText = htmlText
								+ "<div class='p_div' style='background-color:#effefe;font-size:12px;font-family:黑体;height: "
								+ ((parseInt(data[i].m_products[j].p_width) + parseInt(saw_bite)) * w_scale)
								+ "px;width:"
								+ ((parseInt(data[i].m_products[j].p_height) + parseInt(saw_bite)) * h_scale)
								+ "px;margin-top: "
								+ (data[i].m_products[j].m_left * w_scale)
								+ "px;margin-left: "
								+ (data[i].m_products[j].m_top * h_scale)
								+ "px;'><br />&nbsp;&nbsp;"
								+ data[i].m_products[j].p_name
								+ "<br />&nbsp;&nbsp;"
								+ data[i].m_products[j].p_height + "x"
								+ data[i].m_products[j].p_width + "</div>";
					}

					for ( var j = 0; j < data[i].m_y_materials.length; j++) {
						if (0 == data[i].m_y_materials[j].m_is_show) {

							if (60 <= (parseInt(data[i].m_y_materials[j].r_width))
									&& 60 <= (parseInt(data[i].m_y_materials[j].r_height))) {

								htmlText = htmlText
										+ "<div class='p_div' style='font-size:12px;font-family:黑体;background-image:url(wg.png);height: "
										+ ((parseInt(data[i].m_y_materials[j].r_width)) * w_scale)
										+ "px;width:"
										+ ((parseInt(data[i].m_y_materials[j].r_height)) * h_scale)
										+ "px;margin-top: "
										+ (data[i].m_y_materials[j].m_m_left * w_scale)
										+ "px;margin-left: "
										+ (data[i].m_y_materials[j].m_m_top * h_scale)
										+ "px;'>&nbsp;&nbsp;余料:"
										+ parseInt(data[i].m_y_materials[j].r_height)
										+ "x"
										+ parseInt(data[i].m_y_materials[j].r_width)
										+ "</div>";
							}
						}
					}

					htmlText = htmlText + "</div>";

					htmlText = htmlText + "</div></div>";
				}
			} else {
				htmlText = htmlText
						+ "<div class='b_div' style='position: absolute;margin-top:"
						+ (p_no * 749)
						+ "px;width: 1078px;height:746px;background-color:#fff;'>";
				htmlText = htmlText
						+ "<div style='position: absolute;margin-left:1px;margin-top:30px;width: 1077px;height:40px;background-color:#fff;text-align:center;'>板材信息汇总</div>";
				htmlText = htmlText
						+ "<div style='position: absolute;margin-top:70px;margin-left:260px;width: 100px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>厚度</div>";
				htmlText = htmlText
						+ "<div style='position: absolute;margin-top:70px;margin-left:360px;width: 150px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>花色</div>";
				htmlText = htmlText
						+ "<div style='position: absolute;margin-top:70px;margin-left:510px;width: 200px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>板材规格</div>";
				htmlText = htmlText
						+ "<div style='position: absolute;margin-top:70px;margin-left:710px;width: 100px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>数量</div>";
				for ( var j = 0; j < data[i].m_materials.length; j++) {
					htmlText = htmlText
							+ "<div style='position: absolute;margin-top:"
							+ (100 + j * 30)
							+ "px;margin-left:260px;width: 100px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>"
							+ data[i].m_materials[j].m_weight + " mm</div>";
					htmlText = htmlText
							+ "<div style='position: absolute;margin-top:"
							+ (100 + j * 30)
							+ "px;margin-left:360px;width: 150px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>"
							+ data[i].m_materials[j].m_color + "</div>";
					htmlText = htmlText
							+ "<div style='position: absolute;margin-top:"
							+ (100 + j * 30)
							+ "px;margin-left:510px;width: 200px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>"
							+ data[i].m_materials[j].m_height + " * "
							+ data[i].m_materials[j].m_width + "</div>";
					htmlText = htmlText
							+ "<div style='position: absolute;margin-top:"
							+ (100 + j * 30)
							+ "px;margin-left:710px;width: 100px;height:30px;background-color:#fff;text-align:center;border: solid 1px;line-height:30px;'>"
							+ data[i].m_materials[j].m_u_count + " 块</div>";
				}

				htmlText = htmlText + "</div>";

			}
		}

		htmlText = htmlText.replace(/pagecount/g, p_no);

		$("#panel").html(htmlText);
		//alert(data);
	}

	function changeImg(v, i) {
		//alert(v.value);
		if ('1' == v.value) {
			$("img[name=img_" + i + "]").attr("src", "sj.png");
			$("#t_img" + i + "").css("marginLeft","-10px");
			$("#dir" + i + "").css("marginLeft","22px");
		} else {
			$("img[name=img_" + i + "]").attr("src", "yuan.png");
			$("#t_img" + i + "").css("marginLeft","0px");
			$("#dir" + i + "").css("marginLeft","12px");
		}
	}

	function returnInfo() {
		$("#panel").html("");
		$("#iTable").show();

		$("#t_table").show();
		$("#tt_table").show();
		$("#d_table").show();
		$("#b_table").show();

		$("#t_y_table").hide();
		$("#tt_y_table").hide();
		$("#d_y_table").hide();
		$("#b_y_table").hide();
		$("#bc_table").hide();
		$("#bb_table").hide();
	}

	function printInfo() {

		if (confirm("打印后数据将清空，请在打印机连接正确，确保能完成打印的情况下打印，确定要打印吗？")) {
			$("#returninfo").remove();
			$("#print").remove();
			window.print();
		}
	}
</script>
</head>
<body background="bg.jpg">
	<div id="iTable"
		style="margin: 0 auto; width: 1250px; text-align: center; background-color: #91a2c0;">

		<div style="margin-top: 50px; width: 200px;">
			<img src="b_logo.png" width='200' />
		</div>


		<div id="t_table"
			style="margin-top: 30px; width: 1150px; height: 40px; line-height: 40px; font-family: '黑体'; font-size: 20px; background-color: #fff67d; letter-spacing: 2px; border: #005ca7 2px solid;">
			家具构件开料明细&nbsp;<span style="font-family: '黑体'; font-size: 14px;">(单位：</span><span
				style="font-family: '黑体'; font-size: 16px;">mm</span><span
				style="font-family: '黑体'; font-size: 14px;">)</span>
		</div>

		<div id="tt_table"
			style="margin-top: 10px; width: 1150px; border: 2px #005ca7 solid; font-size: 14px;">
			<table cellpadding="0" cellspacing="0" style="font-weight: bold;">
				<tr bgcolor="#d7ecdb">
					<td rowspan="2" class="td" width="250">构件代码</td>
					<td rowspan="2" class="td" width="250">名称</td>
					<td colspan="3" class="td" width="270">规格</td>
					<td rowspan="2" class="td" width="110">花色</td>
					<td rowspan="2" class="td" width="110">数量</td>
					<td rowspan="2" class="td" width="110">纹理</td>
					<td rowspan="2" class="td" width="50">&nbsp;</td>
				</tr>
				<tr bgcolor="#d4dff1">
					<td class="td td_t" width="90">长</td>
					<td class="td td_t" width="90">宽</td>
					<td class="td td_t" width="90">厚</td>
				</tr>
			</table>
		</div>
		<div id="d_table"
			style="margin-top: 5px; width: 1150px; border: 2px #005ca7 solid">
			<table id="table" cellpadding="0" cellspacing="0">
				<tr name="tr1" id="tr1" bgcolor="#ffffff">
					<td width="250" class="td"><span id="p_index1"
						style="margin-left: -30px; width: 20px;">1</span><span
						style="margin-left: 20px;"><input id="product_nos"
							type="text" size="22" /></span></td>
					<td width="250" class="td"><input id="product_names"
						type="text" size="25" /></td>
					<td width="90" class="td"><input id="product_heights"
						type="text" size="4" /></td>
					<td width="90" class="td"><input id="product_widths"
						type="text" size="4" /></td>
					<td width="90" class="td"><input id="product_weights"
						type="text" size="1" /></td>
					<td width="110" class="td"><input id="product_colors"
						type="text" size="10" /></td>
					<td width="110" class="td"><input id="product_counts"
						type="text" size="4" /> 块</td>
					<td width="110" class="td"><span id="t_img1"
						style="position: relative;; margin-top: -5px;margin-left: 0px;"><img
							name="img_1" alt="" width="12" src="yuan.png"></span><span id="dir1"
						style="position: relative; margin-left: 12px;"><select
							style="text-align: center; width: 50px;" id="is_direction"
							onchange="changeImg(this,1)"><option value="1">单向</option>
								<option value="0" selected="selected">混合</option></select></span></td>
					<td width="50">&nbsp;</td>
				</tr>
			</table>
		</div>

		<div id="b_table" style="margin-top: 15px; width: 1150px;">
			<img id="addrow" alt="" src="tj.jpg" width="120" />&nbsp;<img
				id="pro_com" alt="" src="wc.jpg" width="120" />
		</div>


		<div id="t_y_table"
			style="margin-top: 30px; width: 1150px; height: 40px; line-height: 40px; font-family: '黑体'; font-size: 16px; background-color: #fff67d; letter-spacing: 2px;">
			<input id="kc" type="checkbox" style="border: 1px solid;" />&nbsp;库存余料优先
		</div>

		<div id="tt_y_table"
			style="margin-top: 10px; width: 540px; border: 2px #005ca7 solid; font-size: 14px;">
			<table cellpadding="0" cellspacing="0" style="font-weight: bold;">
				<tr bgcolor="#d7ecdb">
					<td colspan="3" class="td" width="270">规格</td>
					<td rowspan="2" class="td" width="110">花色</td>
					<td rowspan="2" class="td" width="110">数量</td>
					<td rowspan="2" class="td" width="50">&nbsp;</td>
				</tr>
				<tr bgcolor="#d4dff1">
					<td class="td td_t" width="90">长</td>
					<td class="td td_t" width="90">宽</td>
					<td class="td td_t" width="90">厚</td>
				</tr>
			</table>
		</div>

		<div id="d_y_table"
			style="margin-top: 5px; width: 540px; border: 2px #005ca7 solid">
			<table id="tablem" cellpadding="0" cellspacing="0">
				<tr name="trm1" id="trm1" bgcolor="#ffffff">
					<td width="90" class="td"><input id="material_heights"
						type="text" size="4" /></td>
					<td width="90" class="td"><input id="material_widths"
						type="text" size="4" /></td>
					<td width="90" class="td"><input id="material_weights"
						type="text" size="1" /></td>
					<td width="110" class="td"><input id="material_colors"
						type="text" size="10" /></td>
					<td width="110" class="td"><input id="material_counts"
						type="text" size="4" /> 块</td>
					<td width="50">&nbsp;</td>
				</tr>
			</table>
		</div>

		<div id="b_y_table" style="margin-top: 15px; width: 650px;">
			<img id="addrowm" alt="" src="tj.jpg" width="120" />
		</div>


		<div id="bc_table"
			style="margin-top: 5px; width: 1150px; border: 2px #005ca7 solid">
			<table align="center" width="1150" cellpadding="0" cellspacing="0"
				style="font-size: 14px; font-family: '黑体';">
				<tr bgcolor="#ffffff">
					<td width="600" align="right">选择板材规格&nbsp;&nbsp;&nbsp;&nbsp;</td>
					<td width="550" align="left"><select style="width: 180px;"
						id="material_name">
							<option value="4 x 8">4 x 8 呎 &nbsp;(1220 x 2440)</option>
							<option value="5 x 8">5 x 8 呎 &nbsp; (1530 x 2440)</option>
							<option value="4 x 9">4 x 9 呎 &nbsp;(1220 x 2750)</option>
							<option value="5 x 9">5 x 9 呎 &nbsp;(1530 x 2750)</option>
							<option value="4 x 10">4 x 10 呎 &nbsp; (1220 x 3060)</option>
							<option value="5 x 10">5 x 10 呎 &nbsp;(1530 x 3060)</option>
					</select></td>
				</tr>
				<tr bgcolor="#d8d9db">
					<td align="right">裁切锯口尺寸&nbsp;&nbsp;&nbsp;&nbsp;</td>
					<td align="left"><input type="text" id="saw_bite" size="2" />
						mm</td>
				</tr>
				<tr bgcolor="#ffffff">
					<td align="right">板材利用率筛选比例&nbsp;&nbsp;</td>
					<td align="left"><input type="text" id="scale" value="0.78"
						size="2" /> (0-1的2位小数)</td>
				</tr>
			</table>
		</div>

		<div id="bb_table" style="margin-top: 15px; width: 1150px;">
			<img id="addbut" src='qrwc.png' width="120" />
		</div>

	</div>
	<div id="loading"
		style="width: 200px; margin: 0 auto; margin-top: 300px;">
		<img src="07.gif" />
	</div>
	<div id="panel" style=""></div>
</body>
</html>