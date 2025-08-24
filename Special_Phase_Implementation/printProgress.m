function printProgress(operation, current, total)
    progressStr = sprintf('操作执行进度 %d/%d\n', current, total);  
    outputStr = strcat(operation, ': ', progressStr);
    disp(outputStr);
end