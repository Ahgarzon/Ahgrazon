function visualizarTablero(individuo)
% Crear una matriz para representar el tablero de ajedrez
  tablero = zeros(8, 8);

% Colocar las reinas en el tablero
  for i = 1:8
      tablero(i, individuo(i)) = 1;
  end

% Crear una imagen en blanco para el tablero
  imagen = ones(8 * 50, 8 * 50, 1);

% Dibujar el tablero en la imagen
  for fila = 1:8
      for columna = 1:8
          if mod(fila + columna, 2) == 0
             % Cuadro blanco
             color = 1;
          else
             % Cuadro negro
             color = 0;
          end
            
          % Dibujar el cuadro
          fila_inicio = (fila - 1) * 50 + 1;
          fila_fin = fila * 50;
          columna_inicio = (columna - 1) * 50 + 1;
          columna_fin = columna * 50;
            
          imagen(fila_inicio:fila_fin, columna_inicio:columna_fin, 1) = color;
      end
  end

% Dibujar las reinas en la imagen
  for fila = 1:8
      for columna = 1:8
          if tablero(fila, columna) == 1
              % Dibujar una reina en la posición correspondiente
              if sum(imagen((fila - 1) * 50 + 1:fila * 50, (columna - 1) * 50 + 1:columna * 50, :)) == 50
                 reina_blanca = imread('reina_blanca.png');
                 imagen((fila - 1) * 50 + 1:fila * 50, (columna - 1) * 50 + 1:columna * 50, :) = reina_blanca(:,:,1);
              else
                 reina_negra = imread('reina_negra.png');
                 imagen((fila - 1) * 50 + 1:fila * 50, (columna - 1) * 50 + 1:columna * 50, :) = reina_negra(:,:,1);
              end
          end
      end
  end

 % Mostrar la imagen del tablero con las reinas
   imshow(imagen);
end