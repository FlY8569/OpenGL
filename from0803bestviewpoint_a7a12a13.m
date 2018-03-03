function [ ] = Untitled3( )
%UNTITLED3 此处显示有关此函数的摘要
%   此处显示详细说明
% [vertex,face]=read_obj('NormalizeModel.obj');
[vertex,face]=read_obj('obj1/Normalize28Mask1.obj');
% [vertex,face]=read_obj('top.obj');
[vbvertex,vbface]=read_obj('viewballmonster.obj');

%%
%--------------------------------------------------------Bunny Pretreatment
sumvbvertexx=0.0;
sumvbvertexy=0.0;
sumvbvertexz=0.0;
for n=1:size(vbvertex,2)
    sumvbvertexx=sumvbvertexx+vbvertex(1,n);
    sumvbvertexy=sumvbvertexy+vbvertex(2,n);
    sumvbvertexz=sumvbvertexz+vbvertex(3,n);
end
originbp=[sumvbvertexx/size(vbvertex,2) sumvbvertexy/size(vbvertex,2) sumvbvertexz/size(vbvertex,3)];

sumvertexx=0.0;
sumvertexy=0.0;
sumvertexz=0.0;
for n=1:size(vertex,2)
    sumvertexx=sumvertexx+vertex(1,n);
    sumvertexy=sumvertexy+vertex(2,n);
    sumvertexz=sumvertexz+vertex(3,n);
end
originp=[sumvertexx/size(vertex,2) sumvertexy/size(vertex,2) sumvertexz/size(vertex,2)];

for n=1:size(vertex,2)
    vertex(1,n)=vertex(1,n)+(originbp(1)-originp(1));
    vertex(2,n)=vertex(2,n)+(originbp(2)-originp(2));
    vertex(3,n)=vertex(3,n)+(originbp(3)-originp(3));
end

%%
mI=compute_barycenter(vertex,face);

vbymax=max(vbvertex(2,:));
vbymin=min(vbvertex(2,:));
pi=3.141592;
vbk=pi/(vbymin-vbymax);
vbb=-vbk*vbymax;
abovepreference=[];
%%
maxdepth=[];

% for n=1:size(eyeface,1)
%     v1index=face(1,eyeface(n,1));
%     v2index=face(2,eyeface(n,1));
%     v3index=face(3,eyeface(n,1));
%     vx1=vertex(1,v1index);
%     vy1=vertex(2,v1index);
%     vz1=vertex(3,v1index);
%     vx2=vertex(1,v2index);
%     vy2=vertex(2,v2index);
%     vz2=vertex(3,v2index);
%     vx3=vertex(1,v3index);
%     vy3=vertex(2,v3index);
%     vz3=vertex(3,v3index);
%     edge1=sqrt((vx1-vx2)^2+(vy1-vy2)^2+(vz1-vz2)^2);
%     edge2=sqrt((vx1-vx3)^2+(vy1-vy3)^2+(vz1-vz3)^2);
%     edge3=sqrt((vx2-vx3)^2+(vy2-vy3)^2+(vz2-vz3)^2);
%     p=(edge1+edge2+edge3)/2;
%     S=sqrt(p*(p-edge1)*(p-edge2)*(p-edge3));
%     eyefacearea=[eyefacearea; S];
% end

for n=1:size(vbvertex,2)
    vby=vbk*vbvertex(2,n)+vbb;
    curviewabovepreference=2*sqrt(2)*pi^(-1.5)*exp(-(8*pi^(-2)*(vby-0.375*pi)^2));
    abovepreference=[abovepreference; curviewabovepreference];

    %%    
    curviewnormal=[vbvertex(1,n) vbvertex(2,n) vbvertex(3,n)];
    curviewvisiblev=[];
    vfindex=0;
    for k=1:size(face,2)
        v1index=face(1,k);
        v2index=face(2,k);
        v3index=face(3,k);
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
        if ((curviewnormal*curnormal)>0)
            curviewvisiblev=[curviewvisiblev; v1index];
            curviewvisiblev=[curviewvisiblev; v2index];
            curviewvisiblev=[curviewvisiblev; v3index];
        else if (abs((curviewnormal*curnormal)-0)<0.5)
                vfindex=k;
            end
        end
    end
    curviewvisiblev=unique(curviewvisiblev,'rows');
    %     -5.83366 -47.7272 39.4789
    %     -5.83366 382.046 39.4789
    
    curview_nearestdis=100000.0;
    curview_nearestid=0;
    for k=1:size(curviewvisiblev,2)
        vindex=curviewvisiblev(k);
        vx=vertex(1,vindex);
        vy=vertex(2,vindex);
        vz=vertex(3,vindex);
        dis=sqrt((vx-curviewnormal(1,1))^2+(vy-curviewnormal(1,2))^2+(vz-curviewnormal(1,3))^2);
        if dis<curview_nearestdis
            curview_nearestdis=dis;
            curview_nearestid=vindex;
        end
    end
    
    if vfindex~=0
        v1index=face(1,vfindex);
        v2index=face(2,vfindex);
        v3index=face(3,vfindex);
        vx1=vertex(1,v1index);
        vy1=vertex(2,v1index);
        vz1=vertex(3,v1index);
        vx2=vertex(1,v2index);
        vy2=vertex(2,v2index);
        vz2=vertex(3,v2index);
        vx3=vertex(1,v3index);
        vy3=vertex(2,v3index);
        vz3=vertex(3,v3index);
        p2=[(vx1+vx2+vx3)/3 (vy1+vy2+vy3)/3 (vz1+vz2+vz3)/3];
        p1p2=[(vertex(1,curview_nearestid)-p2(1,1)); (vertex(2,curview_nearestid)-p2(1,2)); (vertex(3,curview_nearestid)-p2(1,3));];
        curviewdepth=curviewnormal*p1p2/sqrt(curviewnormal(1,1)^2+curviewnormal(1,2)^2+curviewnormal(1,3)^2);
    else
        fprintf('vfindex = 0 size(curviewvisiblev)=%d\n',size(curviewvisiblev));
        curviewdepth=sqrt(curviewnormal(1,1)^2+curviewnormal(1,2)^2+curviewnormal(1,3)^2)-curview_nearestdis;
    end
    maxdepth=[maxdepth; curviewdepth];
 
    %%
%     [lia,~]=ismember(eyeface,curviewvisiblev);
%     cursumeyearea=0.0;
% %     disp(size(lia));
%     for k=1:size(lia,1)
%         if lia(k,1)==1
%             cursumeyearea=cursumeyearea+eyefacearea(k,1);
%         end
%     end
%     eye=[eye; cursumeyearea];
    fprintf('n=%d\n',n)
%     disp('n=');
%     disp(n);
end

% diary on;
% diary monster_a7a12a13
% disp('maxdepth');
% disp(maxdepth);
% disp('abovepreference');
% disp(abovepreference);
% disp('eye');
% disp(eye);
% diary off;

diary on;
diary obj1_attribute/Normalize28Mask1_a7.txt
disp('maxdepth');
disp(maxdepth);
diary obj1_attribute/Normalize28Mask1_a12.txt
disp('abovepreference');
disp(abovepreference);
diary off;

end

