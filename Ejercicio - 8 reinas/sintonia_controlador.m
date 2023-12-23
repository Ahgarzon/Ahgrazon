% *************************************
% Sintonia controlador
% *************************************
clc, close all, clear variables
 
% Configuración Algoritmo Genético
options = optimoptions(@ga);
 
% Población Genética
options = optimoptions(options, 'PopulationSize',2500);              % Tamaño de la población
options = optimoptions(options, 'PopulationType', 'doubleVector'); % Tipo de datos
options = optimoptions(options, 'PopInitRange',[1 1 1 1 1 1 1 1 ; 8 8 8 8 8 8 8 8]); % Rango de inicio
options = optimoptions(options, 'CreationFcn',@gacreationuniform); % Poblacion inicial aleatoria
 
% Criterios de parada
options = optimoptions(options, 'Generations', 50);     % Maximo de Generaciones
options = optimoptions(options, 'FitnessLimit', 1e-4); % Limite de la funcion fitness
 
% Operadores Genéticos
% Operador de selección = Torneo deterministico + aleatorio
options = optimoptions(options, 'SelectionFcn', @selectionroulette);

% Algoritmo de cruce = 1 Punto. Probabilidad de Cruce
options = optimoptions(options, 'CrossoverFcn', @crossoversinglepoint); 
options = optimoptions(options, 'CrossoverFraction', 0.8);
 
% Algoritmo de mutación = Puntual. Probabilidad de Mutacion
options  = optimoptions(options, 'MutationFcn',{@mutationuniform, 0.1});

% Configuracion Salida
options = optimoptions(options, 'Display', 'final');
options = optimoptions(options, 'PlotInterval', 5); 
options = optimoptions(options,'PlotFcns',@gaplotbestf);
% options = optimoptions(options,'OutputFcns',@custOutput_controlador);


%% Ejecución algoritmo
nvar = 8;
[x, fval, reason, output, population, scores] = ga(@fitness_controlador, nvar, options);

%% Resultados
disp('Mejor individuo: ');
disp(round(x));    % Mejor solucion
disp('Ajuste  : ');
disp(fval); % Mejor solucion evaluada en la funcion fitness
visualizarTablero([round(x)]);