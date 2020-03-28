%Plotting Practice Generator 3000!
%Plotting Practice for Exam 1
%Developed by Dr. Kevin Holly
%For BIEN 203: Biomedical Engineering Principles II


uiwait(msgbox(["                                          Welcome to PPG3000!";" ";"                                     The Plotting Practice Program";" ";"                             Created for BIEN 203 by Dr. Kevin Holly";" ";"A randomly generated plot will be displayed upon closing this message box. Your objective is to replicate the given plot. This will be analogous to an Exam 1 problem."],'Plotting Practice Generator 3000!'));

x = 1:.5:100;
y_function = [sinc(x);sin(x);cos(x);sin(x)+cos(x)];
y_type = ["sinc(x)","sin(x)","cos(x)","(sin(x)+cos(x))"];
y_multiplier = 1:10;
y_adder = 1:5;

YN = ceil(rand*length(y_type));
YF = y_function(YN,:);
YM = y_multiplier(ceil(rand*length(y_multiplier)));
YA = y_adder(ceil(rand*length(y_adder)));
YT = y_type(YN);

y = YF*YM+YA;

Line_specifier = ["-" "--" ":" "-."];
Marker_specifier = ['+' 'o' '*' '.' 'x' 's' 'd' 'p' 'h' '<' '>' '^' 'v'];
Color_specifier = ['r' 'g' 'b' 'c' 'm' 'y'];
Title_specifier = ["Title 1" "Example Title" "Random Title" "This is fun" "BIEN 203 is the best" "I love taking exams!"];
XLabel_specifier = ["X axis" "Example XLabel" "Random Label" "Labeling x-axis is fun" "BIEN 203 is the best x-axis" "X is the label"];
YLabel_specifier = ["Y axis" "Example YLabel" "Random Label" "Labeling y-axis is fun" "BIEN 203 is the best y-axis" "Y is the label"];

LS = Line_specifier(ceil(rand*length(Line_specifier)));
MS = Marker_specifier(ceil(rand*length(Marker_specifier)));
CS = Color_specifier(ceil(rand*length(Color_specifier)));
CSM = Color_specifier(ceil(rand*length(Color_specifier)));
CSE = Color_specifier(ceil(rand*length(Color_specifier)));
T = Title_specifier(ceil(rand*length(Title_specifier)));
XL = XLabel_specifier(ceil(rand*length(XLabel_specifier)));
YL = YLabel_specifier(ceil(rand*length(YLabel_specifier)));
CSB = Color_specifier(ceil(rand*length(Color_specifier)));

figure('Name', 'Mimic this figure')
plot(x,y,'Marker',MS,'Color',CS,'LineStyle',LS,'MarkerFaceColor',CSM,'MarkerEdgeColor',CSE)
title(T);
xlabel(XL);
ylabel(YL);
set(gcf,'color',CSB);


uiwait(msgbox(["Create a figure that matches the one displayed";" ";"x = 1:.5:100";['Y = ' num2str(YM) char(YT) '+' num2str(YA)]],'Instructions'));

clearvars -except x y