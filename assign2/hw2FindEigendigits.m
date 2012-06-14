% Machine Learning
% Joseph Perez
% Assignment 2

% This function calculates the eigenvectors and eigenvalues based on the 
% covariance matrix of the input matrix of 1D images. This is calculated 
% utilizing the trick from page 14 of the lecture notes. The second
% parameter takes a number value indicating the number of eigenvectors to
% use.

function [mean_vector, V] =  hw2FindEigendigits(A,num_eigvecs)
[m,n] = size(A);
X = zeros(m,n);
cov_X = zeros(m,m);
V = zeros(m,n);
mean_vector = mean(A');
mean_vector = mean_vector';

for i = 1:n
    X(:,i) = A(:,i)-mean_vector;
end

if (n < m)  % if the number of images is less than the number of pixels
    cov_X = X'*X;
    [V, eig_vals] = eig(cov_X); % calculate the eigenvectors and eigenvalues
    eig_vals = eig(cov_X); % get the eigenvalues in a vector
    
    [b, indx] = sort(eig_vals);
    indx = flipud(indx);
    eig_vals = eig_vals(indx);
    V = V(:,indx);
    
    if(num_eigvecs ~= 0)
        temp = zeros(size(V,1),num_eigvecs);
        for i = 1:num_eigvecs
            temp(:,i) = V(:,i);
        end
        V = X*temp;
    else
        V = X*V;    
    end
    V = V/norm(V);
    
else  % calculate the covariance matrix in the usual method
   cov_X = X*X';
   [V, eig_vals] = eig(cov_X); % calculate the eigenvectors and eigenvalues
   eig_vals = eig(cov_X); % get the eigenvalues in a vector
   
   [b, indx] = sort(eig_vals);
   indx = flipud(indx);
   eig_vals = eig_vals(indx);
   V = V(:,indx);
   
   if(num_eigvecs ~= 0)
       temp = zeros(size(V,1),num_eigvecs);
       for i = 1:num_eigvecs
           temp(:,i) = V(:,i);
       end
       V = temp;
   else
   end
   V = V/norm(V);
end
