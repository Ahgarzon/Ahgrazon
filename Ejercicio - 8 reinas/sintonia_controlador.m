% *************************************
% Sintonia controlador
% *************************************
clc, close all, clear variables
 
% Configuraci�n Algoritmo Gen�tico
options = optimoptions(@ga);
 
% Poblaci�n Gen�tica
options = optimoptions(options, 'PopulationSize',2500);              % Tama�o de la poblaci�n
options = optimoptions(options, 'PopulationType', 'doubleVector'); % Tipo de datos
options = optimoptions(options, 'PopInitRange',[1 1 1 1 1 1 1 1 ; 8 8 8 8 8 8 8 8]); % Rango de inicio
options = optimoptions(options, 'CreationFcn',@gacreationuniform); % Poblacion inicial aleatoria
 
% Criterios de parada
options = optimoptions(options, 'Generations', 50);     % Maximo de Generaciones
options = optimoptions(options, 'FitnessLimit', 1e-4); % Limite de la funcion fitness
 
% Operadores Gen�ticos
% Operador de selecci�n = Torneo deterministico + aleatorio
options = optimoptions(options, 'SelectionFcn', @selectionroulette);

% Algoritmo de cruce = 1 Punto. Probabilidad de Cruce
options = optimoptions(options, 'CrossoverFcn', @crossoversinglepoint); 
options = optimoptions(options, 'CrossoverFraction', 0.8);
 
% Algoritmo de mutaci�n = Puntual. Probabilidad de Mutacion
options  = optimoptions(options, 'MutationFcn',{@mutationuniform, 0.1});

% Configuracion Salida
options = optimoptions(options, 'Display', 'final');
options = optimoptions(options, 'PlotInterval', 5); 
options = optimoptions(options,'PlotFcns',@gaplotbestf);
% options = optimoptions(options,'OutputFcns',@custOutput_controlador);


%% Ejecuci�n algoritmo
nvar = 8;
[x, fval, reason, output, population, scores] = ga(@fitness_controlador, nvar, options);

%% Resultados
disp('Mejor individuo: ');
disp(round(x));    % Mejor solucion
disp('Ajuste  : ');
disp(fval); % Mejor solucion evaluada en la funcion fitness
visualizarTablero([round(x)]);