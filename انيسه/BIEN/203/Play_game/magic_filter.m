function [output] = magic_filter(input)

load('noise');
output = input - noise;

end