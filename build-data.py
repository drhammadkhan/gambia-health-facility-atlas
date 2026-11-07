import json,pathlib
out=pathlib.Path('dist');data=[]
renames={33060:('Bansang General Hospital','Tertiary'),33084:('Farafenni General Hospital','Tertiary'),33100:('Essau District Hospital','Secondary'),33111:('Basse District Hospital','Secondary'),33126:('Edward Francis Small Teaching Hospital','Tertiary'),33129:('Bundung Maternal and Child Health Hospital','Tertiary'),33133:('Kanifing General Hospital','Tertiary'),33143:('Brikama Health Centre','Secondary'),33159:('Bwiam General Hospital','Tertiary')}
for f in json.load(open('data/public-facilities-2019.geojson'))['features']:
 p=f['properties'];typ=p['Facility_type'];name=p['Facility_name'];level='Primary' if typ in ['Clinic','Health Centre (minor)'] else 'Secondary' if typ=='Health Centre (major)' else 'Tertiary' if typ in ['Teaching Hospital','General Hospital Hospital'] else 'Unclassified'
 if f['id'] in renames:name,level=renames[f['id']]
 data.append(dict(id=str(f['id']),name=name,aliases=p['Facility_name']+(' EFSTH Royal Victoria Teaching Hospital' if f['id']==33126 else ''),type=typ,level=level,region=p['Admin1'],ownership=p['Ownership'],lat=p['Lat'],lng=p['Long'],locationSource='2019 public-sector facility database; '+p['LL_source'],locationUrl='https://services.arcgis.com/5T5nSi527N4F7luB/ArcGIS/rest/services/A_spatial_database_of_health_facilities_managed_by_the_public_health_sector_in_sub_Saharan_Africa_WFL1/FeatureServer/0/'+str(f['id']),approx=p['LL_source']=='Geonames',assessed=False,resources={},levelBasis='Grouped from recorded facility type; 2021–2025 strategic plan executive summary. Verify current designation.'))
data.extend([dict(id='njau',name='Njau Health Centre',aliases='Njau',type='Health Centre (designation unconfirmed)',level='Unclassified',region='Central River',ownership='Not documented',lat=13.75,lng=-15.2167,locationSource='Njau locality, not verified facility location',locationUrl='https://nona.net/features/map/placedetail.2212658/Njau/',approx=True,levelBasis='Major/minor designation absent from supplied reports.',assessed=False,resources={})])
rows=[('33060','Yes No Yes No No'),('33111','No No No Yes No'),('33143','No No No No No'),('33129','Yes No Yes Yes Yes'),('33159','No No No No No'),('33126','Yes No Yes No No'),('33100','No No Yes Yes Yes'),('33127','No No No No No'),('33084','Yes No Yes Yes Yes'),('33076','No No Yes Yes Yes'),('33133','Yes No No No Yes'),('njau','No No No No Yes'),('33083','No No No Yes No'),('33136','No No No No No')]
for id,vals in rows:
 f=next(f for f in data if f['id']==id);f['assessed']=True;f['resources']={k:('yes' if v=='Yes' else 'no') for k,v in zip(['photo','cpap','power','solar','water'],vals.split())}
for f in data:
 if f['id'] in ['33126','33060']:f['resources']['surgery']='yes'
 if f['id']=='33126':f['resources']['neonatal']='yes'
neonatal_levels={'33060':'Secondary','33084':'Secondary','33159':'Secondary','33133':'Secondary','33129':'Secondary','33126':'Tertiary'}
for f in data:
 f['generalLevel']=f.pop('level')
 f['generalLevelBasis']=f.pop('levelBasis')
 if f['id'] in ['33126','33060','33084','33159','33133','33129']:
  f['generalLevelEvidence']='Named hospital in strategic plan'
  f['generalLevelBasis']='Named teaching/general hospital in section 2.7.1 (printed p.22); tertiary grouping also supported by section 4.1 (pp.100–102). This is a general-service designation, not a neonatal capability assessment.'
  f['type']='Teaching Hospital' if f['id']=='33126' else 'General Hospital'
 elif f['generalLevel']=='Primary':
  f['generalLevelEvidence']='Derived from historical facility type'
  f['generalLevelBasis']='Historical source type: '+f['type']+'. Mapped to primary under the intended structure in section 4.1 (pp.100–102). Not a verified current facility-level designation.'
  if f['type']=='Health Centre (minor)':f['generalLevelBasis']+=' Source discrepancy: section 2.7.2 (p.23) places minor health centres at secondary level; this view consistently uses section 4.1, which places them at primary level.'
 elif f['generalLevel']=='Secondary':
  f['generalLevelEvidence']='Derived from historical type / district designation'
  f['generalLevelBasis']='Major health centre / district hospital grouping under the intended structure in section 4.1 (pp.100–102). Not a verified current facility-level designation.'
  if f['id'] in ['33100','33111','33143','33083']:f['generalLevelBasis']+=' Section 2.7.1 also names this locality as a regional hospital, but its relationship to the district category is not resolved in the plan. Secondary here follows the explicit section 4.1 major-centre/district grouping.'
 else:f['generalLevelEvidence']='Not established'
 f['generalLevelSource']='https://extranet.who.int/cpcd/sites/default/files/public_file_repository/GMB_Gambia_National-Health-Sector-Strategic-Plan_2021-2025.pdf'
 f['neonatalLevel']=neonatal_levels.get(f['id'],'Primary' if f['assessed'] else 'Unclassified')
 f['neonatalLevelBasis']=('Tertiary neonatal service: HF November 2025 mission report; confirmed in the clinical classification (see Data & sources), 5 November 2026.' if f['id']=='33126' else 'November 2025 neonatal workshop context; level set in the clinical classification (see Data & sources), 5 November 2026.' if f['id'] in neonatal_levels else 'Primary neonatal unit: designated in the clinical classification (see Data & sources), 5 November 2026, for the remaining previously unclassified neonatal assessment facilities.' if f['assessed'] else 'Neonatal care level is not established by the supplied reports or subsequent clarification. Not inferred from general facility type or equipment availability.')
public=json.load(open('data/public-enrichment.json'))
for f in data:
 f['public']=public['facilities'].get(f['id'],{'services':[],'workforce':[],'notes':[]})
json.dump({k:v for k,v in public.items() if k!='facilities'},open(out/'public-sources.json','w'),indent=2,ensure_ascii=False)
import csv
with open(out/'public-records.csv','w',newline='') as stream:
 writer=csv.writer(stream)
 writer.writerow(['Facility ID','Facility','Record type','Service or cadre','Status','Observed headcount','Comparison','Reference minimum (not observed)','Observation date','Source','Source type','Publication date','Source URL','Source location','Scope / note','Accessed'])
 for f in data:
  for kind in ['services','workforce']:
   for r in f['public'][kind]:
    src=public['sources'][r['source']]
    writer.writerow([f['id'],f['name'],kind,public['serviceLabels'].get(r.get('key'),r.get('cadre')),r.get('status',''),r.get('value',''),r.get('operator',''),r.get('referenceMinimum',''),r['asOf'],src['title'],src['kind'],src['published'],src['url'],r.get('locator',''),(r.get('scope','')+' '+r.get('note','')).strip(),public['reviewedAt']])
data.sort(key=lambda f:(not f['assessed'],f['name']))
json.dump(data,open(out/'facilities.json','w'),indent=2)
json.dump({'title':'Facility Resource Assessment Report','date':'12–13 November 2025','author':'Dr Hammad Khan with support from HF Team','columns':['Phototherapy','CPAP','Electricity','Solar','Water'],'records':[{'facility':f['name'],'resources':f['resources']} for f in data if f['assessed']],'notes':['Phototherapy Yes means some but not enough.','No facility reported adequate phototherapy.','Structured CPAP table reports No for all 15. Unattributed workshop comments suggest equipment at some facilities; unresolved conflict.','Electricity and water columns are binary source responses; narratives report intermittency even for some Yes responses.']},open(out/'assessment.json','w'),indent=2)
print('Facilities:',len(data),'assessed:',sum(f['assessed'] for f in data))
