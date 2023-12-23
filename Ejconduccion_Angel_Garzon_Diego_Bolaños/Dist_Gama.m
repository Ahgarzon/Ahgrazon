%  Cálculo de la DISTANCIA  que separa al móvil de su
%  punto final y del ángulo GAMA necesario para calcular
%  el ángulo ALFA, perteneciente al sistema de conducción de un móvil
% u = [ xf ; yf ; xi ; yi ; Phi]
% v = [ Alfa ; Distancia ] 


function v = Dist_Gama(xf, yf, xi, yi, Phi)

% Cálculo de la distancia
  dX        = abs(xf - xi);
  dY        = abs(yf - yi); 
  distancia = sqrt(dX^2 + dY^2);

% Cálculo del cuadrante de operacion
  if (yf >= yi && xf > xi)
      Angulo_cuadrante = 0 ;
      cateto_opuesto   = dY ;
  end
  if (yf >= yi && xf <= xi)
      Angulo_cuadrante = pi/2 ;
      cateto_opuesto   = dX ;
  end
  if (yf < yi  && xf <= xi)
      Angulo_cuadrante = pi ;
      cateto_opuesto   = dY ;
  end
  if (yf < yi  && xf > xi)
      Angulo_cuadrante = 3*pi/2 ;
      cateto_opuesto   = dX ;
  end

% Cálculo del ángulo beta
  Beta      = asin(cateto_opuesto/distancia);
  
% Cálculo del ángulo gama
  Gama      = Beta + Angulo_cuadrante;

% Cálculo de Alfa conservando el rango entre -180 0 180
  Alfa      = Phi - Gama; 
  if  (Alfa > pi)
      Alfa  = Alfa - 2*pi;
  end
  if (Alfa < -pi)
      Alfa  = 2*pi + Alfa;
  end

  v = [distancia; Alfa];
end