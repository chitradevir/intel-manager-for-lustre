#
# INTEL CONFIDENTIAL
#
# Copyright 2013 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related
# to the source code ("Material") are owned by Intel Corporation or its
# suppliers or licensors. Title to the Material remains with Intel Corporation
# or its suppliers and licensors. The Material contains trade secrets and
# proprietary and confidential information of Intel or its suppliers and
# licensors. The Material is protected by worldwide copyright and trade secret
# laws and treaty provisions. No part of the Material may be used, copied,
# reproduced, modified, published, uploaded, posted, transmitted, distributed,
# or disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.


help_text = {
    'advanced_settings': '<b>Use care when changing these parameters as they can significantly impact functionality or performance.</b> For help with these settings, contact your storage solution provider.',
    'bytes_per_inode': 'File system space (in bytes) per MDS inode. The default is 2048, meaning one MDS inode per each 2048 bytes of file system space. In the "Lustre Operations Manual", see Section 5.3.3: Setting the Number of Inodes for the MDS.',
    'commands': 'Shows past and currently running commands that the manager is executing to perform tasks, such as formatting or starting a file system.',
    'command_detail': 'View details about this command.',
    'detect_file_systems-dialog': 'Ensure that all storage servers for mounted Lustre targets in the file system to be detected are up and running. Then select the storage servers (including passive failover servers) and click <b>Run</b> to scan them for existing Lustre targets.',
    'dismiss_message': 'Acknowledge this message and move it to the history view.',
    'goto_dashboard': 'Go to the Dashboard',
    'detect_file_systems-tooltip': 'Detect an existing file system to be monitored at the manager GUI.',
    'inode_size': 'Size (in bytes) of the inodes used to store Lustre metadata on the MDS for each file. The default is 512 bytes. In the "Lustre Operations Manual", see 5.3.1: Setting the Number of Inodes for the MDS.',
    'force_remove': 'This action removes the record for the storage server in the manager database, without attempting to contact the storage server. All targets that depend on this server will also be removed without any attempt to unconfigure them.  <b>You should only perform this action if the server is permanently unavailable.</b>',
    'invoke_agent': 'Indicates that the chroma-agent service can be accessed on this server.',
    'nids': 'The Lustre network identifier(s) for the LNet network(s) to which this node belongs.',
    'ping': 'Indicates if an ICMP ping from the server running Intel(R) Manager for Lustre, to the server, succeeded.',
    'type': 'The type of storage device.',

    'rescan_NIDs-dialog': 'Select all servers for which the server NID may have changed and click <b>Run</b> to re-read the NIDs. <i>Note:</i> After completing this operation, you must update any affected Lustre targets by clicking the <strong>Re-write Target Configuration</strong> button.',
    'remove_server': 'Remove this server. Any file systems or targets that rely on this server will also be removed.',
    'rescan_NIDs-tooltip': 'Query the network interfaces on the storage servers to update the record of NIDs.',
    'auth': 'Indicates if the manager server was able to connect, via SSH, to the storage server using the supplied authentication credentials.',
    'reverse_ping': 'Indicates if an ICMP ping from the storage server to manager server succeeded.',
    'resolve': 'Indicates if a DNS lookup performed at the manager server, of the fully-qualified domain name (FQDN) of the storage server, succeeded.',
    'reverse_resolve': 'Indicates if a DNS lookup by the storage server of the fully-qualified domain name (FQDN) of the manager server succeeded.',
    'hostname_valid': 'Indicates if the self-reported hostname of the storage server is valid (resolves to a non-loopback address).',
    'fqdn_resolves': 'Indicates if a DNS lookup at the manager server, of the self-reported fully-qualified domain name (FQDN) of the storage server, succeeded.',
    'fqdn_matches': 'Indicates if there is match between the DNS lookup at the manager server of the user-supplied hostname, and the DNS lookup at the storage server of the self-reported fully-qualified domain name (FQDN) of the storage server.',
    'rewrite_target_configuration-dialog': 'Select all servers for which the NIDs were re-read by clicking the <strong>Rescan NIDs</strong> button.  Then click <b>Run</b> to rewrite the Lustre target configuration for targets associated with the selected servers.',
    'rewrite_target_configuration-tooltip': 'Update each target with the current NID for the server with which it is associated.',

    'server_status_configured': 'This server has been configured for use with the manager GUI.',
    'server_status_lnet_down': 'The LNet kernel module is loaded, but LNet networking is not currently started on this server.',
    'server_status_lnet_unloaded': 'The LNet kernel module is not currently loaded on this server.',
    'server_status_lnet_up': 'LNet networking is started on this server.',
    'server_status_unconfigured': 'This server has not yet been configured for use with the manager GUI.',

    'state_changed': 'Time at which the state last changed, either detected or as a result of user action.',

    'status': 'Indicates the status of high availability (HA) configuration for this volume (ha = available for HA, noha = not configured for HA).',
    'status_light': 'Indicates current system health. <br /> Green: The file system is operating normally. <br />  Yellow: The system may be operating in a degraded mode. <br /> Red: This system may be down or is severely degraded. <br /> Click to view all system event and alert status messages.',

    'start_file_system': 'Start the metadata and object storage targets so the file system can be mounted by clients.,',
    'stop_file_system': 'Stop the metadata and object storage targets, thus making the file system unavailable to clients.',
    'remove_file_system': 'Remove file system. This file system\'s contents will remain intact until its volumes are reused in another file system.',

    'lnet_state': 'The status of the LNet networking layer on this server.',
    'start_lnet': 'Load the LNet kernel module and start the LNet networking layer.',
    'stop_lnet': 'Shut down the LNet networking layer and stop any targets running on this server.',
    'unload_lnet': 'If LNet is running, stop LNET and unload the LNet kernel module to ensure that it will be reloaded before any targets are started again.',

    'start_mdt': 'Start the metadata target (MDT).',
    'stop_mdt': 'Stop the MDT. When an MDT is stopped, the file system becomes unavailable until the MDT is started again. If an object reference is known to a client, the client can continue to access the object in the file system after the MDT is shut down, but will not be able to obtain new object references.',

    'start_mgt': 'Start the management target (MGT).',
    'stop_mgt': 'Stop the MGT. When an MGT is stopped, clients are unable to make new connections to file systems using the MGT. However, MDT(s) and OST(s) stay up if they have been started and can be stopped and restarted while the MGT is stopped.',
    'remove_mgt': 'Remove this MGT. The contents will remain intact until the volume is reused for a new target.',

    'start_ost': 'Start the object storage target (OST).',
    'stop_ost': 'Stop the OST. When an OST is stopped, clients are unable to access the files stored on this OST.',
    'remove_ost': 'Remove the OST from the file system. This OST will no longer be seen in the manager GUI. <strong>Caution</strong>: When an OST is removed, files stored on the OST will no longer be accessible.<b> To preserve data, manually create a copy of the data elsewhere before removing the OST.</b>',

    'volume_long': 'Volumes (also called LUNs or block devices) are the underlying units of storage used to create Lustre file systems.  Each Lustre target corresponds to a single volume. If servers in the volume have been configured for high availability, primary and secondary servers can be designated for a Lustre target. Only volumes that are not already in use as Lustre targets or local file systems are shown. A volume may be accessible on one or more servers via different device nodes, and it may be accessible via multiple device nodes on the same host.',
    'volume_short': 'A LUN or block device used as a metadata or object storage target in a Lustre file system.',
    'volume_status_configured-ha': 'This volume is ready to be used for a high-availability (HA) Lustre target.',
    'volume_status_configured-noha': 'This volume is ready to be used as a Lustre target, but is not configured for high availability.',
    'volume_status_unconfigured': 'This volume cannot be used as a Lustre target until a primary server is selected.',

    'access_denied_eula': 'To proceed, a superuser must first login and accept the EULA.',

    'eula': """
        <h3>Intel&reg; Enterprise Edition for Lustre* software</h3>
        <h3>End User License Agreement Terms</h3>

        <h4>IMPORTANT - READ BEFORE COPYING, INSTALLING OR USING THE SOFTWARE</h4>

        <p>Do not use or load this software and any associated documentation (collectively, the "Software" or "Materials")
        until you have carefully read the following terms and conditions. By selecting "Agree" below, or by loading or
        using the Software, you agree to the terms of this license agreement (the "License Agreement"). If you do not
        wish to agree, click "Do Not Agree" and do not install or use the Software. If you are an employee or agent of a
        legal entity, you represent and warrant that you have the authority to bind such legal entity to this Agreement.</p>

        <p>The Software includes both open source and proprietary software that are provided by Intel Corporation or its majority-owned
        subsidiaries ("Intel") with this License Agreement, and any other accompanying documentation.
        The open source components include (i) the Intel&reg; Enterprise Edition for Lustre*software (Intel&reg; EE for Lustre* software),
        and (ii) the Intel&reg; Hadoop Adaptor for Lustre* software (collectively, the "Intel Open Source Software").
        The proprietary components include (i) the Intel&reg; Manager for Lustre* software ("Intel Manager") and (ii)
        any other components that are marked as "Intel proprietary" or with a similar legend (collectively, the "Intel Software").</p>

        <ol>
          <li>
            <h5>LICENSE GRANT.</h5>
            <ol>
              <li>Licenses for the Intel Open Source Software.  The Intel Open Source Software will be governed by the open source licenses accompanying such materials.</li>
              <li>License for Intel Proprietary Software.
                <ol class="alpha">
                  <li>Subject to all of the terms and conditions of this Agreement,
                      including any restrictions set forth in Section 2 below,
                      Intel Corporation ("Intel") grants to you a non-exclusive, non-assignable, copyright license to
                      install one copy per license and use the Intel Software on a single server or computer Solely for the
                      purpose of installing, configuring, monitoring and managing a Lustre file system that uses Intel&reg;
                      Enterprise Edition for Lustre* software. Except as expressly provided in this Section 1,
                      you will not have any other rights to the Intel Software.
                  </li>
                  <li>Subject to all of the terms and conditions of this Agreement,
                      including any restrictions set forth in Section 2 below,
                      Intel grants to you a non-exclusive, non-transferable,
                      non-sublicensable license under Intel's Licensed Patent Claims to make one copy per license of the
                      Intel Software internally only, and use the Intel Software internally only. "Licensed Patent Claims"
                      means the claims of Intel's patents that are necessarily and directly infringed by the reproduction of
                      the Intel Software authorized herein, when that Intel Software is in its unmodified form as delivered
                      by Intel to you and not modified, or combined with anything else. Licensed Patent Claims are only
                      those claims which Intel can license without paying, or getting the consent of, a third party.
                  </li>
                </ol>
              </li>
            </ol>
          </li>
          <li><h5>LICENSE RESTRICTIONS.</h5>  You may NOT:  (i) use or copy the Intel Software except as provided in this Agreement; (ii) rent or lease the Intel Software to any third party; (iii) assign this Agreement or transfer the Intel Software without the express written consent of Intel; (iv) modify, adapt, or translate the Intel Software in whole or in part except as provided in this Agreement; (v) reverse engineer, decompile, de-obfuscate or disassemble the Intel Software; (vi) distribute, sublicense or transfer any components of the Intel Software to any third party except as provided in this Agreement; or (vii) modify or distribute the Source Code of any Intel Software so that any part of it becomes subject to an Excluded License.  An "Excluded License" is one that requires, as a condition of use, modification, or distribution, that (a) the code be disclosed or distributed in source code form; or (b) others have the right to modify it.  The Intel Software may include third party programs or materials.  The license terms with those programs or materials apply to your use of them, and Intel is not liable for them.</li>
          <li><h5>OPEN SOURCE SOFTWARE.</h5>  In addition to the Intel Open Source Software, certain programs and or files included with the Software may include Open Source Code (defined below). Your rights to use the Open Source Software are governed by the license agreements that accompany such components. Intel does not warrant such Open Source Software in any way and assumes no liability for your use of the Open Source Software.  You are subject to the terms of their license agreements if you use the Open Source Software.  "Open Source Code" means any software that requires as a condition of use, modification and/or distribution of such software that such software or other software incorporated into, derived from or distributed with such software (a) be disclosed or distributed in source code form; or (b) be licensed by the user to third parties for the purpose of making and/or distributing derivative works; or (c) be redistributable at no charge.  Open Source Software includes, without limitation, software licensed or distributed under any of the following licenses or distribution models, or licenses or distribution models substantially similar to any of the following: (a) GNU's General Public License (GPL) or Lesser/Library GPL (LGPL), (b) the Artistic License (e.g., PERL), (c) the Mozilla Public License, (d) the Netscape Public License, (e) the Sun Community Source License (SCSL), (f) the Sun Industry Source License (SISL), (g) the Apache Software license and (h) the Common Public License (CPL).</li>
          <li><h5>NO OTHER RIGHTS.</h5>  Except as otherwise expressly provided, Intel grants no express or implied right under Intel patents, copyrights, trade secrets, trademarks, or other intellectual property rights. </li>
          <li><h5>OWNERSHIP OF SOFTWARE AND COPYRIGHTS.</h5>  Title to the Materials and all copies thereof remain with Intel or its suppliers.  The Materials are copyrighted and are protected by United States copyright laws and international treaty provisions.  You will not remove any copyright notice from the Materials.  You agree to prevent any unauthorized copying of the Materials.  Except as expressly provided herein, no license or right is granted to you directly or by implication, inducement, estoppel or otherwise, specifically Intel does not grant any express or implied right to you under Intel patents, copyrights, trademarks, or trade secret information.</li>
          <li><h5>NO WARRANTY AND LIMITED REPLACEMENT.</h5>  THE MATERIALS ARE PROVIDED "AS IS", WITH NO WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT OF INTELLECTUAL PROPERTY RIGHTS, OR ANY WARRANTY OTHERWISE ARISING OUT OF ANY PROPOSAL, SPECIFICATION, OR SAMPLE.  If the media on which the Materials are furnished are found to be defective in material or workmanship under normal use for a period of ninety (90) days from the date of receipt, Intel's entire liability and your exclusive remedy shall be the replacement of the media.  This offer is void if the media defect results from accident, abuse, or misapplication.</li>
          <li><h5>LIMITATION OF LIABILITY.</h5>  IN NO EVENT SHALL INTEL OR ITS SUPPLIERS OR VENDORS OR THIRD PARTY SOFTWARE OWNERS BE LIABLE FOR ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, LOST PROFITS, BUSINESS INTERRUPTION, OR LOST INFORMATION) ARISING OUT OF THE USE OF OR INABILITY TO USE THE SOFTWARE, EVEN IF INTEL HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. SOME JURISDICTIONS PROHIBIT EXCLUSION OR LIMITATION OF LIABILITY FOR IMPLIED WARRANTIES OR CONSEQUENTIAL OR INCIDENTAL DAMAGES, SO THE ABOVE LIMITATION MAY NOT APPLY TO YOU. THE WARRANTY DISCLAIMER AND LIMITATIONS ON LIABILITY IN THIS AGREEMENT ARE FUNDAMENTAL ELEMENTS OF THE AGREEMENT BETWEEN INTEL AND YOU REGARDING THE MATERIALS.  INTEL WOULD NOT BE ABLE TO PROVIDE THE MATERIALS TO YOU WITHOUT SUCH LIMITATIONS.</li>
          <li><h5>UNAUTHORIZED USES.</h5>  THE SOFTWARE IS NOT DESIGNED, INTENDED, OR AUTHORIZED FOR USE IN ANY MEDICAL, LIFE SAVING OR LIFE SUSTAINING SYSTEMS, OR FOR ANY OTHER APPLICATION IN WHICH THE FAILURE OF THE SOFTWARE COULD CREATE A SITUATION WHERE PERSONAL INJURY OR DEATH MAY OCCUR. Should You purchase or use the Software for any such unintended or unauthorized use, You shall indemnify and hold Intel and its officers, subsidiaries and affiliates harmless against all claims, costs, damages, and expenses, and reasonable attorney fees arising out of, directly or indirectly, any claim of product liability, personal injury or death associated with such unintended or unauthorized use, even if such claim alleges that Intel was negligent regarding the design or manufacture of the part.</li>
          <li><h5>USER SUBMISSIONS.</h5>  You agree that any material, information or other communication, including all data, images, sounds, text, and other things embodied therein, you transmit or post to an Intel website or provide to Intel under this Agreement will be considered non-confidential ("Communications").  Intel will have no confidentiality obligations with respect to the Communications. You agree that Intel and its designees will be free to copy, modify, create derivative works, publicly display, disclose, distribute, license and sublicense through multiple tiers of distribution and licensees, incorporate and otherwise use the Communications, including derivative works thereto, for any and all commercial or non-commercial purposes.</li>
          <li><h5>CONSENT.</h5> You agree that Intel, its subsidiaries or suppliers may collect and use technical and related information, including but not limited to technical information about your computer, system and application software, and peripherals, that is gathered periodically to facilitate the provision of software updates, product support and other services to you (if any) related to the Software, and to verify compliance with the terms of this Agreement.  Intel may use this information, as long as it is in a form that does not personally identify you, to improve our products or to provide services or technologies to you.</li>
          <li><h5>TERMINATION OF THIS LICENSE.</h5> This Agreement becomes effective on the date you accept this Agreement and will continue until terminated as provided for in this Agreement. If you are using the Software under the control of a time-limited license, for example an Evaluation License, this Agreement terminates without notice on the last day of the time period, which is controlled by the license key code for the Software.  Intel may terminate this license at any time if you are in breach of any of its terms and conditions. Upon termination, you will immediately return to Intel or destroy the Software and all copies thereof.</li>
          <li><h5>APPLICABLE LAWS.</h5> Claims arising under this License Agreement shall be governed by the laws of Delaware, excluding its principles of conflict of laws and the United Nations Convention on Contracts for the Sale of Goods. You may not export the Software in violation of applicable export laws and regulations. Intel is not obligated under any other agreements unless they are in writing and signed by an authorized representative of Intel.</li>
          <li><h5>U.S. GOVERNMENT RESTRICTED RIGHTS.</h5> This Agreement is for Your temporary license of Software for Your internal use.  No Government procurement regulation or contract clauses or provision will be considered a part of any transaction between the Parties under this Agreement unless its inclusion is required by statute, or mutually agreed upon in writing by the Parties in connection with a specific transaction.  The technical data and computer Software covered by this license is a "Commercial Item," as that term is defined by the FAR 2.101 (48 C.F.R. 2.101) and is "commercial computer software" and "commercial computer software documentation" as specified under FAR 12.212 (48 C.F.R. 12.212) or DFARS 227.7202 (48 C.F.R. 227.7202), as applicable.  This commercial computer software and related documentation is provided to end users for use by and on behalf of the U.S. Government, with only those rights as are granted to all other end users under the terms and conditions in this Agreement.  Use for or on behalf of the U.S. Government is permitted only if the party acquiring or using this Software is properly authorized by an appropriate U.S. Government official.</li>
          <li><h5>OTHER GENERAL INFORMATION.</h5> Intel is not responsible for any errors which may appear in the documentation or the Software, nor does Intel make a commitment to update the information or software contained herein. Intel reserves the right to make changes to this document or software at any time, without notice. </li>
        </ol>

        <p>The English language version of this License Agreement shall be the only legally binding version and in the event of a conflict, inconsistency or difference of interpretation between the English language version and any other translation, the English language version shall prevail over such other translation.  Any translation of this License Agreement is provided for convenience only and shall not be used in the interpretation or construction of this License Agreement and shall not be binding on the parties. </p>

        <p class="subtext">Intel and the Intel logo are trademarks or registered trademarks of Intel Corporation or its subsidiaries in the United States and other countries. *Other names and brands may be claimed as the property of others.</p>
    """,
    "continue_as_anonymous": "Click this link to continue as an anonymous user. This user has restricted privileges on how they can use the Intel&reg; Manager for Lustre* software.",
    "no_dismiss_message": "This alert relates to an active problem. When the problem is fixed you may dismiss."
}
