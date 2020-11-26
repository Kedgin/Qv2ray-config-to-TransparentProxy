# Qv2ray-config-to-TransparentProxy

Normal Qv2ray cannot get things done at some situations. Sometimes a transparent proxy is essential.

I successfully use this method to built a transparent proxy: https://toutyrater.github.io/app/tproxy.html

Thanks, ToutyRater.

This python script converts Qv2ray config file to fit the transparent proxy requirements.

Here are some detail of my circumstance.

1. Before install Qv2ray, I installed v2ray from this link https://github.com/v2fly/fhs-install-v2ray . 
So I can "systemctl start v2ray" to use v2ray. But I cannot update the servers by a subscription link. 
It's very inconvenient to me.

2. After installed Qv2ray, I disabled v2ray server from auto start.

    systemctl stop v2ray
    
    systemctl disable v2ray
    
I only use Qv2ray most of time. 

3. If I need a transparent proxy I execute the following steps:

    a. Stop Qv2ray. (I use kill command in Linux, because it run in the background after I close the GUI.)
    
    b. Conver the configuration.
    
        sudo python3 convert2TransparentConfig.py -i qv2rayconfigfilename -o config.json -t template.json
        
        Then copy config.json to the directory which v2ray require.
        
        Or modify the default value in convert2TransparentConfig.py to fit your env:
        
            source_config_file = '/home/username/.config/qv2ray/generated/config.gen.json'
                
            dest_config_file = '/usr/local/etc/v2ray/config.json'
            
            template_config_file = 'template.json'

        and execute the script without any parameter.
        
            sudo python3 convert2TransparentConfig.py
    
    c. Execute all commands in "iptables.cmd" file.
    
    d. Start v2ray. (systemctl start v2ray)

4. If I want to switch back to normal state I execute the following steps:

    a. Stop v2ray. (systemctl stop v2ray)
    
    b. Remove mangle table of iptables.
    
        iptables -t mangle -F
        
        iptables -t mangle -X
        
      If you already have items in mangle before 3 step c, don't do that. You have to delete those items that you added, not the whole table.
      
    c. Start Qv2ray.
