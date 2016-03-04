function DXDsvd
  lam = 1;
  load 'multilingual.D.mat'
  D2 = D;
  D1 = D;

  load 'multilingual.X.de.mat'
  total = X;
%  load 'multilingual.X.el.mat'
%  total = total + X;
  load 'multilingual.X.en.mat'
  total = total + X;
  load 'multilingual.X.es.mat'
  total = total + X;
%  load 'multilingual.X.fi.mat'
%  total = total + X;
  load 'multilingual.X.fr.mat'
  total = total + X;
%  load 'multilingual.X.hu.mat'
%  total = total + X;
  load 'multilingual.X.it.mat'
  total = total + X;
  load 'multilingual.X.pt.mat'
  total = total + X;
  load 'multilingual.X.sv.mat'
  total = total + X;
  X = total;

  [ m, n ] = size(X);
  nnzX = nnz(X);
  nnzD1 = nnz(D1);
  nnzD2 = nnz(D2);
  P1 = speye(m) + lam*D1; P2 = speye(n) + lam*D2; 
  clear D1 D2;

  r = 40;
  opts.issym = 1;
  opts.isreal= 1;
  tic
  [ Q, D ] = eigs( @(u)DXDu( X, P1, P2, u, m, n ), m+n, 2*r, 'LM', opts );
  Ss = D(1:r,1:r);
  Vs = sqrt(2)*Q(1:n,1:r);
  Us = sqrt(2)*Q(n+1:n+m,1:r);
  t = toc;
  save('DXDsvd40lam1.mat', 'Us', 'Ss', 'Vs', 'lam')
% We actually only use 'Us' and scipy/octave handle structs badly
% so save 'Us' separately as ascii to be loaded with np.loadtxt
  save('-ascii', 'DXDsvd40lam1_ascii_Us.mat', 'Us')
  save('timing.mat', 'nnzX', 'nnzD1', 'nnzD2', 't');
exit;
end

function u = DXDu( X, P1, P2, u, m, n )
  u1 = u(1:n); u2 = u(n+1:m+n);
  uu1 = P2* ( X'* (P1'*u2) );
  uu2 = P1* ( X * (P2'*u1) );
  u = [ uu1; uu2 ];
end
