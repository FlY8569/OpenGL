function [ ] = visibleFace( )

%   求出所有可见面
[vertex,face]=read_obj('bird.obj');    %读入
mi=[mean(vertex(1,:)),mean(vertex(2,:)),mean(vertex(3,:))]; % 求平均值坐标（x,y,z)

plot_mesh(vertex,face);

plot3([mi(1) 0],[mi(2) 0],[mi(3) 0],'r-');

m=1;
vpnormal=[0;0;abs(mi(3)*3)];
for n=1:size(face,2)   %返回矩阵x的列数
    v1index=face(1,m);
    v2index=face(2,m);
    v3index=face(3,m);
    vx1=vertex(1,v1index);
    vy1=vertex(2,v1index);
    vz1=vertex(3,v1index);
    vx2=vertex(1,v2index);
    vy2=vertex(2,v2index);
    vz2=vertex(3,v2index);
    vx3=vertex(1,v3index);
    vy3=vertex(2,v3index);
    vz3=vertex(3,v3index);
    a = (vy1 - vy2)*(vz1 - vz3) - (vy1 - vy3)*(vz1 - vz2);
    b = (vz1 - vz2)*(vx1 - vx3) - (vx1 - vx2)*(vz1 - vz3);
    c = (vx1 - vx2)*(vy1 - vy3) - (vx1 - vx3)*(vy1 - vy2);
    curnormal=[a;b;c];
    
    if ((dot(curnormal,vpnormal))<=0)   %列向量的点乘
            face(:,m)=[];
            m=m-1;
    end
    m=m+1;
end
plot_mesh(vertex,face);
fprintf('1face.size=%d\n m=%d\n',size(face,2),m);

visiblev=[];

for n=1:size(face,2);
    visiblev=[visiblev; face(1,n); face(2,n); face(3,n)];
end

visiblev=unique(visiblev);
fprintf('visiblev.size=%d\n',size(visiblev,1));
% disp(visiblev);

unvisiblevid=[];
for n=1:size(visiblev,1)
    vindex=visiblev(n);
    vx=vertex(1,vindex);
    vy=vertex(2,vindex);
    vz=0.0;
    p=[vx; vy; vz];
    for k=1:size(face,2)
        v1index=face(1,k);
        v2index=face(2,k);
        v3index=face(3,k);
        if v1index==vindex||v2index==vindex||v3index==vindex
            break;
        end
        vx1=vertex(1,v1index);
        vy1=vertex(2,v1index);
        vz1=0.0;
        vx2=vertex(1,v2index);
        vy2=vertex(2,v2index);
        vz2=0.0;
        vx3=vertex(1,v3index);
        vy3=vertex(2,v3index);
        vz3=0.0;
        
        a=[vx1; vy1; vz1];
        b=[vx2; vy2; vz2];
        c=[vx3; vy3; vz3];
        
        if SameSide(a,b,c,p)&&SameSide(b,c,a,p)&&SameSide(c,a,b,p)
            %in triangle
%             fprintf('vindex=%d in the triangle\n',vindex);
            if vertex(3,vindex)<=mean([vertex(3,v1index) vertex(3,v2index) vertex(3,v3index)])
                unvisiblevid=[unvisiblevid; vindex];
            end
        end
    end
end
fprintf('unvisiblevid.size=%d\n',size(unvisiblevid,1));

[lia,~]=ismember(face,unvisiblevid);
m=1;
for n=1:size(lia,2)
    for k=1:3
        if lia(k,n)==1
            face(:,m)=[];
            m=m-1;
            break;
        end
    end
    m=m+1;
end
fprintf('2face.size=%d\n',size(face,2));
plot_mesh(vertex,face);

%diary on;
%diary bird.txt
%disp('face');
%disp(face);
%diary off;

end

function [flag]= SameSide(A,B,C,P)
ab=A-B;
ac=C-A;
ap=P-A;
v1=cross(ab,ac);
v2=cross(ab,ap);
flag=(dot(v1,v2)>0);
end
