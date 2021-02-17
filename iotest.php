<?php
    define('__ROOT__', dirname(__FILE__));
    require_once(__ROOT__.'/config.php'); 

    $getPinstatus = 'undefined';
    $status = (object) array('status' => 'error', 'message' => '');

    // set port and status
    $pin = 17;
    $state = 0;

    // Set I/O mode for pin
    trim(@shell_exec("gpio -g mode $pin out"));

    // write out status to gpio port
    $string = "gpio -g write $pin $state";
    $val = trim(@shell_exec("$string"));
    
    // read status of gpio port
    exec("gpio read $gpioConnectors[$pin]", $pinStatus);
    
    // error handling of read command
    if(is_array($pinStatus) && isset($pinStatus[0])) {
        $getPinstatus = intval($pinStatus[0]);
        $status->status = 'success';
        $status->message = 'state changed';
        $status->touchedpin = $pin;
    }
    
    // return result as json object
    $status->hardwarestatus = $getPinstatus;
    echo json_encode ($status, true);
    
    exit(0);
?>
