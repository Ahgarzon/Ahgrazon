function [ FitnessValue ] = fitness_damas(x_pop)
bandera=false;
n_pop = round(x_pop);
pos_Damas = zeros(8,2);

if length(unique(n_pop)) < 8
    s = 500;
else 
    for x=1:8
        pos_Damas(x,:)= [n_pop(x),x];
%         if i == 8
%             disp(n_pop)
%         disp(pos_Damas)
%         end


    end
    for i = 1:7
        for j = i+1:8
            if abs(pos_Damas(i,1) - pos_Damas(j,1)) == abs(pos_Damas(i,2) - pos_Damas(j,2))
                s = 500;
                bandera=true;

            elseif i == 7 && j == 8 && bandera==false
                s = 0.1;
                disp(pos_Damas)
                
            end
        end
    end    
end


FitnessValue = s;


