//JS necesario para cortar a 200 caracteres lo que se muestran en las tablas: aca recortamos por ej. la Descripcion de la tabla de puestos vista en http://localhost:8000/listar/puestos/

var len = 200;
var table = document.getElementById("truncateMe");  
for (var i = 0, row; row = table.rows[i]; i++) {      //Iteramos sobre las row de las tablas
   for (var j = 0, col; col = row.cells[j]; j++) {    //Iteramos sobre las td. col sería nuestras td de las table.
      if (col) {
      var trunc = col.innerHTML;
         if (trunc.length > len) {

          trunc = trunc.substring(0, len);
          trunc = trunc.replace(/\w+$/, '');


          trunc += '<a href="#" ' +
            'onclick="this.parentNode.innerHTML=' +
            'unescape(\''+escape(col.innerHTML)+'\');return false;">' +
            '...<\/a>';
          col.innerHTML = trunc;
         }
      }
   }  
}