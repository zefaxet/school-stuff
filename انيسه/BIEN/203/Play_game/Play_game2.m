% %    player = audioplayer(signal,fs);
% %    play(player)
% %    stop(player)
   
   disp('>>%Let''s listen to our signal!')
   pause(2)
   disp('>>%I''m going to let player = audioplayer(signal,fs);')
   pause(2)
   player = audioplayer(signal,fs);
   disp('>>play(player)')
   input('>>')
   
   disp('>>%The NOISE!!! MUST STOP!!!')
   pause(2)
   disp('>>stop(player)')
   input('>>')
   
   disp('>>%The signal is noisy... Filter time!')
   pause(2)
   
    
   %magic filter!
   disp('>>%Setting new_signal = magic_filter(signal);')
   new_signal = magic_filter(signal);
  
%    plot(1:length(signal(1:15000)),signal(1:15000));


% %    axis_handle = gca;
% %    axis_handle.Children.YData = new_signal(1:15000);

  disp('>>%Ok, I''m done playing repeat after me...')
  pause(2)
  disp('>>%Update the plot by using axis_handle.Children.YData and then follow the instructions given by Dr. Holly.')
   
  msgbox(["You have now entered the open ended section of the signal processing game, again.";"";"Objective: Please consult with Dr. Holly about the next task. He should provide you with a set of instructions."],'The Open-ended Signal Processing Game!');

   
     
% %    player2 = audioplayer(new_signal,fs);
% %    play(player2)
% %    stop(player2)
