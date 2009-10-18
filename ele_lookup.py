import pygoogleearth
import re
from optparse import OptionParser

def getEle (lat, lon, ge):
    """
    Given the gearth object and a lat lon
    return altitude
    """
    ge.set_camera_params(lat, lon, alt=0, alt_mode=1)
    pt = ge.get_point_on_terrain_from_screen_coords(0,0)
    return pt.Altitude

def getCoordStr(kml):
    """
    return coords string from kml
    """
    match = re.match(r"[\s\S]+\<coordinates\>([\s\S]+)\</coordinates\>[\s\S]+", data)
    return match.group(1)

def getCoords(coord_str):
    """
    return coords as list
    """
    regex2 = re.compile('\s+')
    s = regex2.split(coord_str)
    coord_list = []
    for i in s:
        coord_list.append(i.split(','))
    return coord_list

def insertEle(coord_list, ge):
    """
    take coord_list
    return coord_list with elevations 
    """
    for i in coord_list:
        if (len(i) == 3):
            ele = getEle(i[1], i[0], ge)
            i[2] = ele
    return coord_list

def convertListToStr(coord_list):
    """
    Take a coord_list and convert to a kml coord string
    """
    coord_str = ""
    for i in coord_list:
        if (len(i) == 3):
            coord_str += str(i[0])
            coord_str += ','
            coord_str += str(i[1])
            coord_str += ','
            coord_str += str(i[2])
            coord_str += ' '
    return coord_str

def replaceCoordStr(coord_str_ele, kml):
    """
    Replace the coordinates in the kml with coord_str
    """
    # split at <coordinates>
    kml_1 = kml.split("<coordinates>")
    kml_2 = kml.split("</coordinates>")
    # insert coord_str_ele
    new_kml = kml_1[0] + '<coordinates>' +coord_str_ele + '</coordinates>' + kml_2[1]
    return new_kml
    

if __name__ == '__main__':

    #options    
    parser = OptionParser()
    parser.add_option("-i", "--input-file", dest="input_file",
                  help="kml file to read from", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_file",
                  help="kml output file", metavar="OUTPUT")
    (options, args) = parser.parse_args()
    
    ge = pygoogleearth.GoogleEarth()
    # test case, uncomment to make sure its working
    #print getEle(ge, -41.288658, 174.707336)
    
    f = open(options.input_file, 'r')
    data = f.read()
    coord_str = getCoordStr(data)
    coord_list = getCoords(coord_str)

    
    #test_list = [[''], ['174.707336', '-41.288658', '20'], ['174.709625', '-41.290798', '30']]
    # this bit is slow as it calls gearth
    coord_list_ele = insertEle(coord_list,ge)
    coord_str_ele = convertListToStr(coord_list_ele)
    
    f = open(options.output_file, 'w')
    new_data = replaceCoordStr(coord_str_ele, data)
    f.write(new_data)
    