clear;clc;
conn = sqlite('nanostructures.db');

specific_wavelengths = [0.4e-6, 0.6e-6];
wavelength_list = join(string(specific_wavelengths), ",");

query = sprintf( ...
    "SELECT n.structure_info, m.wavelength, m.phase_shift, m.transmission " + ...
    "FROM measurements m " + ...
    "JOIN nanostructures n ON m.structure_id = n.id " + ...
    "WHERE m.wavelength IN (%s) " + ...
    "ORDER BY n.structure_info;", wavelength_list);

data = fetch(conn, query);

check=data(:,"phase_shift");
a=table2array(check(5,1));