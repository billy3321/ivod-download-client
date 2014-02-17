<?php
$extensions = array(
      "bcmath",
      "curl",
      "SimpleXML"
);
foreach ($extensions as $extension)
  if (!extension_loaded($extension)){
      echo "You don't have '$extension' extension installed. please install it before continuing.\n";
      exit(1);
  }
exit(0);

?>
