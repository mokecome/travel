def get_one_json(times_now, places,spend_times,all_time):
    import time
    start_time=time.strftime("%H:%M", time.localtime())
    one_data_json = {"type": "bubble",
                    "size": "mega",
                    "header": {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [
                        {
                          "type": "box",
                          "layout": "vertical",
                          "contents": [
                            {
                              "type": "text",
                              "text": "啟程",
                              "color": "#ffffff66",
                              "size": "sm"
                            },
                            {
                              "type": "text",
                              "text": places[0],
                              "color": "#ffffff",
                              "size": "xl",
                              "flex": 4,
                              "weight": "bold"
                            }
                          ]
                        },
                        {
                          "type": "box",
                          "layout": "vertical",
                          "contents": [
                            {
                              "type": "text",
                              "text": "前往",
                              "color": "#ffffff66",
                              "size": "sm"
                            },
                            {
                              "type": "text",
                              "text": places[-1],
                              "color": "#ffffff",
                              "size": "xl",
                              "flex": 4,
                              "weight": "bold"
                            }
                          ]
                        }
                      ],
                      "paddingAll": "20px",
                      "backgroundColor": "#0367D3",
                      "spacing": "md",
                      "height": "154px",
                      "paddingTop": "22px"
                    },
                    "body": {
                      "type": "box",
                      "layout": "vertical",
                      "contents": [
                        {
                          "type": "text",
                          "text": all_time[0],
                          "color": "#b7b7b7",
                          "size": "xs"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "text",
                              "text": start_time,
                              "size": "sm",
                              "gravity": "center"
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "filler"
                                },
                                {
                                  "type": "box",
                                  "layout": "vertical",
                                  "contents": [],
                                  "cornerRadius": "30px",
                                  "height": "12px",
                                  "width": "12px",
                                  "borderColor": "#EF454D",
                                  "borderWidth": "2px"
                                },
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 0
                            },
                            {
                              "type": "text",
                              "text": places[0],
                              "gravity": "center",
                              "flex": 4,
                              "size": "sm"
                            }
                          ],
                          "spacing": "lg",
                          "cornerRadius": "30px",
                          "margin": "xl"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "baseline",
                              "contents": [
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 1
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "box",
                                  "layout": "horizontal",
                                  "contents": [
                                    {
                                      "type": "filler"
                                    },
                                    {
                                      "type": "box",
                                      "layout": "vertical",
                                      "contents": [],
                                      "width": "2px",
                                      "backgroundColor": "#B7B7B7"
                                    },
                                    {
                                      "type": "filler"
                                    }
                                  ],
                                  "flex": 1
                                }
                              ],
                              "width": "12px"
                            },
                            {
                              "type": "text",
                              "text": spend_times[0],
                              "gravity": "center",
                              "flex": 4,
                              "size": "xs",
                              "color": "#8c8c8c"
                            }
                          ],
                          "spacing": "lg",
                          "height": "64px"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": times_now[0],
                                  "gravity": "center",
                                  "size": "sm"
                                }
                              ],
                              "flex": 1
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "filler"
                                },
                                {
                                  "type": "box",
                                  "layout": "vertical",
                                  "contents": [],
                                  "cornerRadius": "30px",
                                  "width": "12px",
                                  "height": "12px",
                                  "borderWidth": "2px",
                                  "borderColor": "#6486E3"
                                },
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 0
                            },
                            {
                              "type": "text",
                              "text": places[1],
                              "gravity": "center",
                              "flex": 4,
                              "size": "sm"
                            }
                          ],
                          "spacing": "lg",
                          "cornerRadius": "30px"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "baseline",
                              "contents": [
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 1
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "box",
                                  "layout": "horizontal",
                                  "contents": [
                                    {
                                      "type": "filler"
                                    },
                                    {
                                      "type": "box",
                                      "layout": "vertical",
                                      "contents": [],
                                      "width": "2px",
                                      "backgroundColor": "#6486E3"
                                    },
                                    {
                                      "type": "filler"
                                    }
                                  ],
                                  "flex": 1
                                }
                              ],
                              "width": "12px"
                            },
                            {
                              "type": "text",
                              "text": spend_times[1],
                              "gravity": "center",
                              "flex": 4,
                              "size": "xs",
                              "color": "#8c8c8c"
                            }
                          ],
                          "spacing": "lg",
                          "height": "64px"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "text",
                              "text": times_now[1],
                              "gravity": "center",
                              "size": "sm"
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "filler"
                                },
                                {
                                  "type": "box",
                                  "layout": "vertical",
                                  "contents": [],
                                  "cornerRadius": "30px",
                                  "width": "12px",
                                  "height": "12px",
                                  "borderColor": "#6486E3",
                                  "borderWidth": "2px"
                                },
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 0
                            },
                            {
                              "type": "text",
                              "text": places[2],
                              "gravity": "center",
                              "flex": 4,
                              "size": "sm"
                            }
                          ],
                          "spacing": "lg",
                          "cornerRadius": "30px"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "baseline",
                              "contents": [
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 1
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "box",
                                  "layout": "horizontal",
                                  "contents": [
                                    {
                                      "type": "filler"
                                    },
                                    {
                                      "type": "box",
                                      "layout": "vertical",
                                      "contents": [],
                                      "width": "2px",
                                      "backgroundColor": "#6486E3"
                                    },
                                    {
                                      "type": "filler"
                                    }
                                  ],
                                  "flex": 1
                                }
                              ],
                              "width": "12px"
                            },
                            {
                              "type": "text",
                              "text": spend_times[2],
                              "gravity": "center",
                              "flex": 4,
                              "size": "xs",
                              "color": "#8c8c8c"
                            }
                          ],
                          "spacing": "lg",
                          "height": "64px"
                        },
                        {
                          "type": "box",
                          "layout": "horizontal",
                          "contents": [
                            {
                              "type": "box",
                              "layout": "horizontal",
                              "contents": [
                                {
                                  "type": "text",
                                  "text": times_now[2],
                                  "gravity": "center",
                                  "size": "sm"
                                }
                              ],
                              "flex": 1
                            },
                            {
                              "type": "box",
                              "layout": "vertical",
                              "contents": [
                                {
                                  "type": "filler"
                                },
                                {
                                  "type": "box",
                                  "layout": "vertical",
                                  "contents": [],
                                  "cornerRadius": "30px",
                                  "width": "12px",
                                  "height": "12px",
                                  "borderWidth": "2px",
                                  "borderColor": "#EF454D"
                                },
                                {
                                  "type": "filler"
                                }
                              ],
                              "flex": 0
                            },
                            {
                              "type": "text",
                              "text": places[-1],
                              "gravity": "center",
                              "flex": 4,
                              "size": "sm"
                            }
                          ],
                          "spacing": "lg",
                          "cornerRadius": "30px"
                        }
                      ]
                    }
                  }
    return one_data_json

import requests
import parsel
def get_img_files(dec):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    img_url='https://travel.yam.com/find/{}'.format(dec)
    response1 = requests.get(url=img_url, headers=headers)
    html_data1 = response1.text
    selector1 = parsel.Selector(html_data1)
    title= selector1.css('div.article_list_box_info h3 a::text').get()
    title_url= selector1.css('div.article_list_box a::attr(href)').get()
    lis1 = selector1.css('div.article_list_box a img::attr(src)').get()
    return title,lis1,'https://travel.yam.com/'+title_url
def travel_json(dec,answer):
    title,img_url,tag1_url=get_img_files(dec)
    travel_data_json={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": img_url,
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": title,
                    "size": "xxl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": answer,
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "weight": "regular",
                    "offsetTop": "xs",
                    "offsetBottom": "xl"
                  }
                ]
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "23px"
          }
        ],
        "paddingAll": "0px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "了解更多",
              "uri": tag1_url
            },
            "height": "sm"
          }
        ]
      }
    }
  ]
}
    return travel_data_json
import json
print(json.dumps(get_one_json(['5','4','3'],['7','8','9','10'],['11','12','13'],['1'])))

