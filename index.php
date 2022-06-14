<?php
  $resultado = "";
  if( $_SERVER['REQUEST_METHOD']=="POST" && isset($_POST["param1"]) && isset($_POST["param2"]) && isset($_POST["param3"]) ){
    $command = escapeshellcmd('python main.py "'.$_POST['param1'].'" "'.$_POST['param2'].'" "'.$_POST['param3'].'"');
    $resultado = shell_exec($command);
    unset($_POST["param1"]);
    unset($_POST["param2"]);
    unset($_POST["param3"]);
  }

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Evita reenviar el formulario cuando se recarga la página-->
    <script>
        if ( window.history.replaceState ) {
            window.history.replaceState( null, null, window.location.href );
        }
    </script>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto sistemas inteligentes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" >
</head>
<body>
    <div class="row" >
        <nav class="navbar" style="background-color: #ff7e2f; minheight: 10vh;">
        <a class="navbar-brand" href="index.php">
            <img src="vairaNav.png"  width="50" height="50" style="margin-left: 8px;margin-top: -5px" class="d-inline-block align-top" alt="">
        </a>
        <form class="d-flex" action="../services/cerrar.php">
            <button class="btn btn-primary cerrarSesionBtn"  style="margin-right: 8px;" type="submit"><i class="fa fa-sign-out" aria-hidden="true"> Regresar a punto de venta</i></button>
        </form>
        </nav>
    </div>
    <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="POST">
        <div class="mb-3">
          <label for="exampleInputEmail1" style="margin-left:10px;margin-top:10px;" class="form-label">Nombre del producto</label>
          <input type="text" name="param1" style="margin-left:10px;margin-right:20px;margin-top:10px;"  class="form-control" id="exampleInputEmail1" >
          <label for="exampleInputEmail2" style="margin-left:10px;margin-top:10px;"  class="form-label">Precio</label>
          <input type="text" name="param2" style="margin-left:10px;margin-top:10px;"  class="form-control" id="exampleInputEmail1" >
          <label for="exampleInputEmail2" style="margin-left:10px;margin-top:10px;"  class="form-label">Proveedor</label>
          <input type="text" name="param3" style="margin-left:10px;margin-top:10px;"  class="form-control" id="exampleInputEmail1" >
        </div>
        <button type="submit" class="btn btn-success" style="margin-left: 10px">Buscar categoria</button>
      </form>
      <br>
      <label for="resultado" style="margin-left: 10px"> La categoria sugerida es: <?php echo($resultado); ?></label>
      <br>
      <button type="submit" class="btn btn-success" style="margin-left: 10px;margin-top:10px">¿Deseas guardar tu producto en esta categoria?</button>
      <br>
      <br>
      <br>
      
</body>
</html>