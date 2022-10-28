import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql


class TICEntry(sa.Model):
    __tablename__ = "ticentries"

    id = sa.Column(sa.BigInteger())
    version = sa.Column(sa.BigInteger())
    hip = sa.Column(sa.BigInteger())
    tyc = sa.Column(sa.Text())
    ucac = sa.Column(sa.Text())
    twomass = sa.Column(sa.Text())
    sdss = sa.Column(sa.Text())
    allwise = sa.Column(sa.Text())
    gaia = sa.Column(sa.Text())
    apass = sa.Column(sa.Text())
    kic = sa.Column(sa.BigInteger())
    objtype = sa.Column(sa.Text())
    typesrc = sa.Column(sa.Text())
    ra = sa.Column(psql.DOUBLE_PRECISION())
    dec = sa.Column(psql.DOUBLE_PRECISION())
    posflag = sa.Column(sa.Text())
    pmra = sa.Column(psql.DOUBLE_PRECISION())
    e_pmra = sa.Column(psql.DOUBLE_PRECISION())
    pmdec = sa.Column(psql.DOUBLE_PRECISION())
    e_pmdec = sa.Column(psql.DOUBLE_PRECISION())
    pmflag = sa.Column(sa.Text())
    plx = sa.Column(psql.DOUBLE_PRECISION())
    e_plx = sa.Column(psql.DOUBLE_PRECISION())
    parflag = sa.Column(sa.Text())
    gallong = sa.Column(psql.DOUBLE_PRECISION())
    gallat = sa.Column(psql.DOUBLE_PRECISION())
    eclong = sa.Column(psql.DOUBLE_PRECISION())
    eclat = sa.Column(psql.DOUBLE_PRECISION())
    bmag = sa.Column(sa.Float())
    e_bmag = sa.Column(sa.Float())
    vmag = sa.Column(sa.Float())
    e_vmag = sa.Column(sa.Float())
    umag = sa.Column(sa.Float())
    e_umag = sa.Column(sa.Float())
    gmag = sa.Column(sa.Float())
    e_gmag = sa.Column(sa.Float())
    rmag = sa.Column(sa.Float())
    e_rmag = sa.Column(sa.Float())
    imag = sa.Column(sa.Float())
    e_imag = sa.Column(sa.Float())
    zmag = sa.Column(sa.Float())
    e_zmag = sa.Column(sa.Float())
    jmag = sa.Column(sa.Float())
    e_jmag = sa.Column(sa.Float())
    hmag = sa.Column(sa.Float())
    e_hmag = sa.Column(sa.Float())
    kmag = sa.Column(sa.Float())
    e_kmag = sa.Column(sa.Float())
    twomflag = sa.Column(sa.Text())
    prox = sa.Column(sa.Float())
    w1mag = sa.Column(sa.Float())
    e_w1mag = sa.Column(sa.Float())
    w2mag = sa.Column(sa.Float())
    e_w2mag = sa.Column(sa.Float())
    w3mag = sa.Column(sa.Float())
    e_w3mag = sa.Column(sa.Float())
    w4mag = sa.Column(sa.Float())
    e_w4mag = sa.Column(sa.Float())
    gaiamag = sa.Column(sa.Float())
    e_gaiamag = sa.Column(sa.Float())
    tmag = sa.Column(sa.Float())
    e_tmag = sa.Column(sa.Float())
    tessflag = sa.Column(sa.Text())
    spflag = sa.Column(sa.Text())
    teff = sa.Column(sa.Float())
    e_teff = sa.Column(sa.Float())
    logg = sa.Column(sa.Float())
    e_logg = sa.Column(sa.Float())
    mh = sa.Column(sa.Float())
    e_mh = sa.Column(sa.Float())
    rad = sa.Column(sa.Float())
    e_rad = sa.Column(sa.Float())
    mass = sa.Column(sa.Float())
    e_mass = sa.Column(sa.Float())
    rho = sa.Column(sa.Float())
    e_rho = sa.Column(sa.Float())
    lumclass = sa.Column(sa.Text())
    lum = sa.Column(sa.Float())
    e_lum = sa.Column(sa.Float())
    d = sa.Column(sa.Float())
    e_d = sa.Column(sa.Float())
    ebv = sa.Column(sa.Float())
    jmag = sa.Column(sa.Float())
    e_jmag = sa.Column(sa.Float())
    hmag = sa.Column(sa.Float())
    e_hmag = sa.Column(sa.Float())
    kmag = sa.Column(sa.Float())
    e_kmag = sa.Column(sa.Float())
    twomflag = sa.Column(sa.Text())
    prox = sa.Column(sa.Float())
    w1mag = sa.Column(sa.Float())
    e_w1mag = sa.Column(sa.Float())
    w2mag = sa.Column(sa.Float())
    e_w2mag = sa.Column(sa.Float())
    w3mag = sa.Column(sa.Float())
    e_w3mag = sa.Column(sa.Float())
    w4mag = sa.Column(sa.Float())
    e_w4mag = sa.Column(sa.Float())
    gaiamag = sa.Column(sa.Float())
    e_gaiamag = sa.Column(sa.Float())
    tmag = sa.Column(sa.Float())
    e_tmag = sa.Column(sa.Float())
    tessflag = sa.Column(sa.Text())
    spflag = sa.Column(sa.Text())
    teff = sa.Column(sa.Float())
    e_teff = sa.Column(sa.Float())
    logg = sa.Column(sa.Float())
    e_logg = sa.Column(sa.Float())
    mh = sa.Column(sa.Float())
    e_mh = sa.Column(sa.Float())
    rad = sa.Column(sa.Float())
    e_rad = sa.Column(sa.Float())
    mass = sa.Column(sa.Float())
    e_mass = sa.Column(sa.Float())
    rho = sa.Column(sa.Float())
    e_rho = sa.Column(sa.Float())
    lumclass = sa.Column(sa.Text())
    lum = sa.Column(sa.Float())
    e_lum = sa.Column(sa.Float())
    d = sa.Column(sa.Float())
    e_d = sa.Column(sa.Float())
    ebv = sa.Column(sa.Float())
    e_ebv = sa.Column(sa.Float())
    numcont = sa.Column(sa.BigInteger())
    contratio = sa.Column(sa.Float())
    disposition = sa.Column(sa.Text())
    duplicate_id = sa.Column(sa.BigInteger())
    priority = sa.Column(sa.Float())
    eneg_ebv = sa.Column(sa.Float())
    epos_ebv = sa.Column(sa.Float())
    ebvflag = sa.Column(sa.Text())
    eneg_mass = sa.Column(sa.Float())
    epos_mass = sa.Column(sa.Float())
    eneg_rad = sa.Column(sa.Float())
    epos_rad = sa.Column(sa.Float())
    eneg_rho = sa.Column(sa.Float())
    epos_rho = sa.Column(sa.Float())
    eneg_logg = sa.Column(sa.Float())
    epos_logg = sa.Column(sa.Float())
    eneg_lum = sa.Column(sa.Float())
    epos_lum = sa.Column(sa.Float())
    eneg_dist = sa.Column(sa.Float())
    epos_dist = sa.Column(sa.Float())
    distflag = sa.Column(sa.Text())
    eneg_teff = sa.Column(sa.Float())
    epos_teff = sa.Column(sa.Float())
    teffflag = sa.Column(sa.Text())
    gaiabp = sa.Column(sa.Float())
    e_gaiabp = sa.Column(sa.Float())
    gaiarp = sa.Column(sa.Float())
    e_gaiarp = sa.Column(sa.Float())
    gaiaqflag = sa.Column(sa.BigInteger())
    starchareflag = sa.Column(sa.Text())
    vmagflag = sa.Column(sa.Text())
    bmagflag = sa.Column(sa.Text())
    splists = sa.Column(sa.Text())
    e_ra = sa.Column(psql.DOUBLE_PRECISION())
    e_dec = sa.Column(psql.DOUBLE_PRECISION())
    ra_orig = sa.Column(psql.DOUBLE_PRECISION())
    dec_orig = sa.Column(psql.DOUBLE_PRECISION())
    e_ra_orig = sa.Column(psql.DOUBLE_PRECISION())
    e_dec_orig = sa.Column(psql.DOUBLE_PRECISION())
    raddflag = sa.Column(sa.BigInteger())
    wdflag = sa.Column(sa.BigInteger())

    @classmethod
    def select_from_fields(cls, *fields: str):
        return sa.select(*[getattr(cls, field) for field in fields])
