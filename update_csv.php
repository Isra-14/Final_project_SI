<?php
function process_csv($file, $data) {
 
    $file = fopen($file, "a");

    if(!$file) {
        echo "Error opening file";
        exit;
    }
   
    foreach($data as $line) {
        fputcsv($file, $line);
    }

    fclose($file);
    return 'success';
   }

?>