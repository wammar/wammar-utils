% adapted from the original implementation of Gardner et al. (EMNLP 2015).
function DXDsvd(r, input_mat_filename, temp1_filename, temp2_filename, output_mat_filename, varargin)
  lam = 1;

  % the matrix D is written only once for all languages
  load input_mat_filename
  D2 = D;
  D1 = D;

  % the matrix X is written separately for each language. The filename suffix for all languages are given as a variable-length argument in this function.
  nVarargs = length(varargin);
  fprintf('Number of languages: %d.\n',nVarargs)
  for k = 1:nVarargs
    cooccurence_filename = sprintf('%s%s', input_mat_filename, varargin{k})
    load cooccurence_filename
    if exist('total','var')
      total = X;
    else
      total = total + X;
    end
  end

  % done reading all cooccurence matrices
  X = total;

  [ m, n ] = size(X);
  nnzX = nnz(X);
  nnzD1 = nnz(D1);
  nnzD2 = nnz(D2);
  P1 = speye(m) + lam*D1; P2 = speye(n) + lam*D2; 
  clear D1 D2;

  opts.issym = 1;
  opts.isreal= 1;
  tic
  [ Q, D ] = eigs( @(u)DXDu( X, P1, P2, u, m, n ), m+n, 2*r, 'LM', opts );
  Ss = D(1:r,1:r);
  Vs = sqrt(2)*Q(1:n,1:r);
  Us = sqrt(2)*Q(n+1:n+m,1:r);
  t = toc;
  save(temp2_filename, 'nnzX', 'nnzD1', 'nnzD2', 't');
  save(temp1_filename, 'Us', 'Ss', 'Vs', 'lam')

  % We actually only use 'Us' and scipy/octave handle structs badly
  % so save 'Us' separately as ascii to be loaded with np.loadtxt
  save('-ascii', output_mat_filename, 'Us')
exit;
end

function u = DXDu( X, P1, P2, u, m, n )
  u1 = u(1:n); u2 = u(n+1:m+n);
  uu1 = P2* ( X'* (P1'*u2) );
  uu2 = P1* ( X * (P2'*u1) );
  u = [ uu1; uu2 ];
end
