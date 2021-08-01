#Read CSV and assign column names to ROUTE DataFrame
FILENAME = 'ROUTE0'
ROUTE = read.csv(paste('CSVs/',FILENAME,'.csv',sep=''),stringsAsFactors = FALSE)
ROUTE = ROUTE[order(ROUTE$fid),]
FID = unique(ROUTE$fid)
ROUTEPOINTS = data.frame(FID,t(sapply(FID, function(x) {
  CHKVEC = which(ROUTE$fid==x)
  ROUTE$mgrs[c(min(CHKVEC),max(CHKVEC))]
})),stringsAsFactors = FALSE)
colnames(ROUTEPOINTS) = c('FID','START','END')

#Since the Features may not neccesarily follow alignment of highway
#These loops try to reorder them

#Collect Start and End Points of Segments and Get Ordered Feature ID (FID)
TEMPDF = ROUTEPOINTS[1,]
for(INDEX in 2:nrow(ROUTEPOINTS)){
  TEMPROW = ROUTEPOINTS[which(TEMPDF$END[INDEX-1]==ROUTEPOINTS$START)[1],]
  if(!any(is.na(TEMPROW))){
    TEMPDF[INDEX,] = TEMPROW
  }else{
    TEMPDF[INDEX,] = ROUTEPOINTS[INDEX,]
  }
  rownames(TEMPDF)=1:nrow(TEMPDF)
}
FID = TEMPDF$FID

#Use the reordered FID to reorder ROUTE DataFrame
TEMPDF = ROUTE[1,]
for(fid in FID){
  TEMPDF = rbind(TEMPDF,ROUTE[which(ROUTE$fid==fid),])
}
ROUTE = TEMPDF

#Assuming the coordinates are now in order of the alignment the following
#Line of code separates mgrs to three columns namely
#GRID, EASTING, NORTHING
ROUTE[c('GRID','EASTING','NORTHING')] = t(sapply(ROUTE$mgrs,function(x) c(substr(x,1,5),substr(x,6,10),substr(x,11,15))))

#Rename Columns of ROUTE
#x-> LONGITUDE
#y-> LATITUDE
#fid-> FID
#FEATURES -> FEATURE
#Remove columns
#Length, mgrs
ROUTE = ROUTE[c(1,3,5,4,7,8,9)]
colnames(ROUTE) = c('FID','FEATURE','LONGITUDE','LATITUDE','GRID','EASTING','NORTHING')

#Save ROUTEDF
write.csv(ROUTE,paste('CSVs/',FILENAME,'COORDS.csv',sep=''),row.names = FALSE)