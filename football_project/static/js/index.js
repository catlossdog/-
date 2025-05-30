$(function () {
    echart_1();
    echart_2();
    echart_3();

    function echart_1() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart_1'));
        var xAxisData = ['小组赛', '16强', '8强', '4强', '半决赛', '决赛']; // 欧冠赛程阶段[1,8](@ref)
        var legendData = ['欧冠', '英超', '欧联杯']; // 三大赛事类型[3](@ref)
        var title = "关键进攻指标趋势"; // 更新标题[7](@ref)
        var serieData = [];
        var metaDate = [
            [3.2, 2.9, 2.3, 2.9, 2.8, 2.9],  // 欧冠场均进球
            [2.8, 2.6, 2.5, 3.2, 2.5, 2.9],  // 英超场均进球
            [2.5, 2.9, 2.1, 2.9, 2.2, 2.6]   // 欧联杯场均进球
        ];
        
        for (var v = 0; v < legendData.length; v++) {
            var serie = {
                name: legendData[v],
                type: 'line',
                symbol: "circle",
                symbolSize: 10,
                data: metaDate[v]
            };
            serieData.push(serie);
        }
        var colors = ["#036BC8", "#FFF", "#5EBEFC", "#2EF7F3"];
        var option = {
            // backgroundColor: '#0f375f',
            title: {
                text: title,
                textAlign: 'left',
                textStyle: {
                    color: "#fff",
                    fontSize: "12",
                    fontWeight: "bold"
                }
            },
            legend: {
                show: true,
                left: "center",
                data: legendData,
                y: "5%",
                itemWidth: 18,
                itemHeight: 12,
                textStyle: {
                    color: "#fff",
                    fontSize: 14
                },
            },
            toolbox: {
                orient: 'vertical',
                right: '1%',
                top: '20%',
                iconStyle: {
                    color: '#fff',
                    borderColor: '#fff',
                    borderWidth: 1,
                },
                feature: {
                    saveAsImage: {},
                    magicType: {
                        // show: true,
                        type: ['line','bar','stack','tiled']
                    }
                }
            },
            color: colors,
            grid: {
                left: '2%',
                top: "12%",
                bottom: "5%",
                right: "5%",
                containLabel: true
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
            },
            xAxis: [{
                type: 'category',
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#6173A3'
                    }
                },
                axisLabel: {
                    interval: 0,
                    textStyle: {
                        color: '#9ea7c4',
                        fontSize: 12
                    }
                },
                axisTick: {
                    show: false
                },
                data: xAxisData,
            }, ],
            yAxis: [{
                axisTick: {
                    show: false
                },
                splitLine: {
                    show: false
                },
                axisLabel: {
                    textStyle: {
                        color: '#9ea7c4',
                        fontSize: 12
                    }
                },
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#6173A3'
                    }
                },
            }, ],
            series: serieData
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }

    function echart_2() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart_2'));  
        var giftImageUrl = "data:image/png;base64,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";
        myChart.setOption({
            graphic: {
                elements: [{
                    type: 'image',
                    style: {
                        image: giftImageUrl,
                        width: 30,
                        height: 30
                    },
                    left: '73%',
                    top: 'center'
                }]
            },
            tooltip: {
                trigger: 'axis',
            },

            grid: {
                left: '1%',
                right: '60%',
                top: '10%',
                bottom: '10%',
                containLabel: true,
            },
            xAxis: {
                type: 'value',
                name: 'OEPM值', // 参考网页6的进攻效率指标
                position:'top',
                axisLabel: { color: '#9ea7c4' },
                axisLine: { lineStyle: { color: '#6173A3' } }
            },
            yAxis: {
                type: 'category',
                data: ['约基奇(掘金)','加兰(骑士)','阿伦(骑士)','哈利伯顿(步行者)','亚历山大(雷霆)'],
                axisTick: {
                    show: false
                },
                splitLine: {
                    show: false
                },
                axisLabel: {
                    textStyle: {
                        color: '#9ea7c4',
                        fontSize: 12
                    }
                },
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#6173A3'
                    }
                },
            },
            series: [{
                name: '进攻效率值',
                itemStyle: {
                    normal: {
                        color: function(params) {
                            // build a color map as your need.
                            var colorList = [
                                '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                                '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                                '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                            ];
                            return colorList[params.dataIndex]
                        },
                        shadowBlur: 20,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                type: 'bar',
                data: [85,91,87,89,90]
            },{
                type: 'pie',
                radius: [30, '80%'],
                center: ['75%', '50%'],
                roseType: 'radius',
                color: [ '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'],
                data: [
                    {value:28.6, name:'约基奇\nxG28.6'}, // 预期进球值
                    {value:25.8, name:'加兰\n突破84次'},
                    {value:23.7, name:'阿伦\n头球62%'},
                    {value:24.1, name:'哈利伯顿\n助攻12.5'}, // 网页6助攻数据[6](@ref)
                    {value:22.2, name:'亚历山大\n抢断2.8'}
                ],
                label: {
                    formatter: '{b}:\n{d}%' // 显示球员关键数据维度
                },
                labelLine: {
                    normal: {
                        smooth: true,
                        lineStyle: {
                            width: 2
                        }
                    }
                },
                itemStyle: {
                    normal: {
                        shadowBlur: 30,
                        shadowColor: 'rgba(0, 0, 0, 0.4)'
                    }
                },
       
                animationType: 'scale',
                animationEasing: 'elasticOut',
                animationDelay: function(idx) {
                    return Math.random() * 200;
                }
            }]
        });
    }

    function echart_3() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('chart_3'));  
        
        option = {
            // backgroundColor: "#404A59",
            color: ["#D22F2B", "#6CABDD", "#FFD700"], // 利物浦红、曼城蓝、阿森纳金
        
            title: [{
                text: '',
                left: '1%',
                top: '6%',
                textStyle: {
                    color: '#fff'
                }
            }, {
                text: '',
                left: '83%',
                top: '6%',
                textAlign: 'center',
                textStyle: {
                    color: '#fff',
                    fontSize: 16
                }
            }],
            tooltip: {
                trigger: 'axis',
                formatter: function(params) {
                    let res = `<div style="border-bottom:1px solid #666;padding-bottom:5px;margin-bottom:5px">${params[0].name}月</div>`;
                    params.forEach(item => {
                        res += `${item.marker} ${item.seriesName}<br/>
                        ▸当前积分：${item.value}<br/>
                        ▸场均进球：${item.data.avgGoals}<br/>
                        ▸零封率：${item.data.cleanSheets}%<br/><br/>`;
                    });
                    return res;
                }
            },
            legend: {
                data: ['利物浦', '曼城', '阿森纳'],
                textStyle: {
                    color: '#fff',
                    fontSize: 14
                }
            },
            grid: {
                left: '1%',
                right: '28%',
                top: '16%',
                bottom: '6%',
                containLabel: true
            },
            toolbox: {
                "show": false,
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                data: ['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May']
            },
            
            yAxis: {
                "axisLine": {
                    lineStyle: {
                        color: '#fff'
                    }
                },
                splitLine: {
                    show: false,
                    lineStyle: {
                        color: '#fff'
                    }
                },
                "axisTick": {
                    "show": false
                },
                axisLabel: {
                    textStyle: {
                        color: '#fff'
                    }
                },
                type: 'value'
            },
            series: [{
                name: '利物浦',
                smooth: true,
                type: 'line',
                symbolSize: 9,
                  symbol: 'circle',
                  data: [
                    {value:6, avgGoals:2.8, cleanSheets:60},
                    {value:16, avgGoals:3.1, cleanSheets:55},
                    {value:28, avgGoals:2.9, cleanSheets:50}, 
                    {value:40, avgGoals:3.0, cleanSheets:48},
                    {value:53, avgGoals:3.2, cleanSheets:45},
                    {value:65, avgGoals:3.3, cleanSheets:43},
                    {value:75, avgGoals:3.4, cleanSheets:40},
                    {value:82, avgGoals:3.2, cleanSheets:38},
                    {value:87, avgGoals:3.0, cleanSheets:35},
                    {value:90, avgGoals:2.9, cleanSheets:33}
                ]
            }, 
            {
                name: '曼城',
                smooth: true,
                type: 'line',
                symbolSize: 9,
                  symbol: 'circle',
                  data: [
                    {value:4, avgGoals:2.1, cleanSheets:40},
                    {value:12, avgGoals:2.3, cleanSheets:38},
                    {value:22, avgGoals:2.4, cleanSheets:35},
                    {value:33, avgGoals:2.5, cleanSheets:33},
                    {value:43, avgGoals:2.6, cleanSheets:30},
                    {value:52, avgGoals:2.7, cleanSheets:28},
                    {value:60, avgGoals:2.8, cleanSheets:25},
                    {value:67, avgGoals:2.7, cleanSheets:23},
                    {value:73, avgGoals:2.6, cleanSheets:20},
                    {value:78, avgGoals:2.5, cleanSheets:18}
                ]
            }, 
            {
                name: '阿森纳',
                smooth: true,
                type: 'line',
                symbolSize: 9,
                  symbol: 'circle',
                  data: [
                    {value:7, avgGoals:2.5, cleanSheets:55},
                    {value:17, avgGoals:2.7, cleanSheets:52},
                    {value:29, avgGoals:2.8, cleanSheets:50},
                    {value:41, avgGoals:2.9, cleanSheets:47},
                    {value:54, avgGoals:3.0, cleanSheets:45},
                    {value:66, avgGoals:3.1, cleanSheets:42},
                    {value:76, avgGoals:3.0, cleanSheets:40},
                    {value:83, avgGoals:2.9, cleanSheets:38},
                    {value:89, avgGoals:2.8, cleanSheets:35},
                    {value:93, avgGoals:2.7, cleanSheets:33}
                ]
            }, 
            {
                type: 'pie',
                center: ['83%', '33%'],
                radius: ['30%', '35%'],
                label: {
                    normal: {
                        position: 'center'
                    }
                },
                data: [{
                    value: 63,
                    name: '进攻效率',
                    label: {
                        formatter: 'xG转化率\n{d}%',
                        textStyle: { color: '#fff' }
                    },
                    itemStyle: { color: '#32CD32' }
                }, {
                    value: 37,
                    name: '占位',
                    label: { formatter: '\n预期进球\n(xG 58.7)' }
                }]
            },
        
        
            {
                type: 'pie',
                center: ['83%', '72%'],
                radius: ['30%', '35%'],
                label: {
                    normal: {
                        position: 'center'
                    }
                },
                data: [{
                    value: 435,
                    name: '销售分析',
                    itemStyle: {
                        normal: {
                            color: '#4834CB'
                        }
                    },
                    label: {
                        normal: {
                            formatter: '{d} %',
                            textStyle: {
                                color: '#fff',
                                fontSize: 14
        
                            }
                        }
                    }
                }, {
                    value: 100,
                    name: '占位',
                    tooltip: {
                        show: false
                    },
                    itemStyle: {
                        normal: {
                            color: '#fff'
        
        
                        }
                    },
                    label: {
                        normal: {
                            textStyle: {
                                color: '#fff',
                            },
                            formatter: '\n销售方向'
                        }
                    }
                }]
            }]
        }

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    }
});