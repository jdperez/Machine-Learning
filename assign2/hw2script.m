% Machine Learning
% Joseph Perez
% Assignment 2: Eigendigits

clear;
load hw2.mat;

% This value initalizes the number of training images to use and how much
% to increase it by. 
test_iters = [1:1:10]';
num_test = size(test_iters,1);
classify_acc = zeros(num_test,2);
classify_acc(:,2) = test_iters;

for j = 1:num_test
    %num_training_images = test_iters(j,1);
    num_training_images = 1000; 
    num_pixels = 28*28;
    num_of_interest = 8;
    cnt = 1;
    
    for i=1:num_training_images
        image = reshape(trainImages(1:28,1:28,i),784,1);
        image = cast(image,'double');
        A(:,i) = image;
    end
    
    [mean_vec, V] = hw2FindEigendigits(A,test_iters(j,1));
    
    B = zeros(size(V,2),num_training_images);
    for i = 1:num_training_images
        train_image = reshape(trainImages(1:28,1:28,i),784,1);
        train_image = cast(train_image,'double');
        train_image = train_image - mean_vec;
        train_image = V'*train_image;
        B(:,i) = train_image;
    end
    
    C = [];
    num_test_images = 1000;
    for i = 1:num_test_images
        image = reshape(testImages(1:28,1:28,i),784,1);
        image = cast(image,'double');
        image = image - mean_vec;
        image_project = V'*image;
        C = [C image_project];
        if (size(C,2) == 1)
           reconstructed_image = V*image_project;
           %imshow(reshape(reconstructed_image,28,28));
           %imwrite(4*reshape(reconstructed_image,28,28),'30eigvecs_num7.gif','gif');
        end
    end;
    
    group = (trainLabels(1,1:num_training_images));
    group = cast(group,'double'); 
    num_classify_correct = 0;
    for i = 1:num_test_images
        class = knnclassify(C(:,i)', B', group);
        if (class == testLabels(1,i))
            num_classify_correct = num_classify_correct + 1;
        end
    end
    classify_acc(j,1) = num_classify_correct/num_test_images;

end


    